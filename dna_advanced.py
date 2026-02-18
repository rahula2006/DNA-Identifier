"""
Advanced DNA Profiling Tool
20 STR Markers (CODIS standard) with statistical analysis
"""

import csv
import sys
import math
from collections import Counter

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python dna_advanced.py database.csv sequence.txt")
        print("Example: python dna_advanced.py databases/codis_20.csv sequences/unknown.txt")
        sys.exit(1)

    print("\n" + "="*60)
    print("🧬 ADVANCED DNA PROFILING TOOL")
    print("="*60)
    print(f"Database: {sys.argv[1]}")
    print(f"Sequence: {sys.argv[2]}")
    print("-" * 60)

    # Read database CSV file
    database = []
    with open(sys.argv[1], 'r') as file:
        reader = csv.DictReader(file)
        str_markers = reader.fieldnames[1:]  # All columns except 'name'
        
        for row in reader:
            # Convert STR counts from strings to integers
            for marker in str_markers:
                if row[marker] not in ['X', 'Y']:  # Handle sex chromosomes
                    row[marker] = int(row[marker])
            database.append(row)
    
    print(f"📊 Loaded {len(database)} individuals from database")
    print(f"🧬 STR Markers: {len(str_markers)} markers (CODIS standard)")
    print(f"   Markers: {', '.join(str_markers[:5])}... (showing first 5)")

    # Read DNA sequence file
    with open(sys.argv[2], 'r') as file:
        dna_sequence = file.read().strip()
    
    print(f"📏 DNA sequence length: {len(dna_sequence):,} bases")

    # Calculate longest run for each STR
    print("\n🔍 Analyzing STR repeats...")
    str_counts = {}
    
    for marker in str_markers:
        # Skip sex chromosomes (not STRs)
        if marker == 'AMEL':
            str_counts[marker] = analyze_amelogenin(dna_sequence)
            print(f"   {marker}: {str_counts[marker]}")
        else:
            count = longest_match(dna_sequence, marker)
            str_counts[marker] = count
            print(f"   {marker}: {count} repeats")

    print("\n📋 Matching against database...")
    
    # Store all matches with similarity scores
    matches = []
    
    for person in database:
        match_score = 0
        mismatches = []
        
        for marker in str_markers:
            if marker == 'AMEL':
                if person[marker] == str_counts[marker]:
                    match_score += 1
                else:
                    mismatches.append(marker)
            else:
                # Calculate similarity (allow small differences for degraded samples)
                diff = abs(person[marker] - str_counts[marker])
                if diff == 0:
                    match_score += 1
                elif diff <= 2:
                    match_score += 0.5  # Partial match for degraded DNA
                    mismatches.append(f"{marker}(+/-{diff})")
                else:
                    mismatches.append(f"{marker}({person[marker]}vs{str_counts[marker]})")
        
        similarity = (match_score / len(str_markers)) * 100
        matches.append({
            'name': person['name'],
            'similarity': similarity,
            'mismatches': mismatches
        })
    
    # Sort matches by similarity (highest first)
    matches.sort(key=lambda x: x['similarity'], reverse=True)
    
    # Display top matches
    print("\n" + "-" * 60)
    print("📊 MATCH RESULTS")
    print("-" * 60)
    
    for i, match in enumerate(matches[:5]):  # Show top 5 matches
        print(f"\n{i+1}. {match['name']}")
        print(f"   Similarity: {match['similarity']:.1f}%")
        if match['mismatches'] and len(match['mismatches']) < 5:
            print(f"   Differences: {', '.join(match['mismatches'][:5])}")
        elif match['mismatches']:
            print(f"   Differences: {', '.join(mismatches[:5])}...")
    
    # Determine if there's a match
    best_match = matches[0]
    
    print("\n" + "="*60)
    print("🔬 FORENSIC ANALYSIS")
    print("="*60)
    
    if best_match['similarity'] >= 95:
        print(f"\n✅ POSITIVE IDENTIFICATION: {best_match['name']}")
        print(f"   Confidence: {best_match['similarity']:.1f}%")
        
        # Calculate random match probability
        probability = calculate_match_probability(str_counts, str_markers)
        print(f"\n📈 Random Match Probability: 1 in {probability:,.0f}")
        
        if probability > 1e9:
            print("   💪 This is stronger than a perfect fingerprint match!")
        
    elif best_match['similarity'] >= 70:
        print(f"\n⚠️ POSSIBLE MATCH: {best_match['name']}")
        print(f"   Confidence: {best_match['similarity']:.1f}%")
        print("   ⚠️  Further testing recommended (DNA may be degraded)")
    else:
        print("\n❌ NO MATCH IN DATABASE")
        print("   The DNA profile does not match any individual in the database")
    
    print("\n" + "="*60)


def longest_match(sequence, subsequence):
    """
    Returns length of longest run of subsequence in sequence.
    Optimized for multiple STR markers.
    """
    longest_run = 0
    sub_length = len(subsequence)
    seq_length = len(sequence)

    # Early exit if subsequence longer than sequence
    if sub_length > seq_length:
        return 0

    # Use a sliding window approach
    i = 0
    while i < seq_length - sub_length:
        count = 0
        
        # Check consecutive matches
        while i + (count + 1) * sub_length <= seq_length:
            start = i + count * sub_length
            end = start + sub_length
            
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        
        if count > 0:
            longest_run = max(longest_run, count)
            i += count * sub_length  # Skip past this run
        else:
            i += 1

    return longest_run


def analyze_amelogenin(sequence):
    """
    Determine sex from AMEL marker
    X: 212bp, Y: 218bp fragments
    """
    # Simplified: check for Y chromosome markers
    if "Y" in sequence or "TAT" in sequence:  # Simplified detection
        return "XY"
    return "XX"


def calculate_match_probability(str_counts, markers):
    """
    Calculate random match probability using product rule
    Simplified allele frequencies (in reality would use population database)
    """
    probability = 1.0
    
    # Typical allele frequencies for common STRs (simplified)
    for marker in markers:
        if marker == 'AMEL':
            continue
        # Assume average allele frequency of 0.1 for simplicity
        freq = 0.1
        probability *= freq
    
    # Convert to 1 in X format
    return int(1 / probability)


if __name__ == "__main__":
    main()