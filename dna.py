"""
DNA Profiling Tool - Identifies individuals based on Short Tandem Repeats (STRs)
"""

import csv
import sys

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        print("Example: python dna.py databases/small.csv sequences/1.txt")
        sys.exit(1)

    print(f"\n🧬 DNA Profiling Tool")
    print(f"Database: {sys.argv[1]}")
    print(f"Sequence: {sys.argv[2]}")
    print("-" * 40)

    # Read database CSV file
    database = []
    with open(sys.argv[1], 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert STR counts from strings to integers
            for key in row:
                if key != 'name':
                    row[key] = int(row[key])
            database.append(row)
    
    print(f"📊 Loaded {len(database)} individuals from database")

    # Read DNA sequence file
    with open(sys.argv[2], 'r') as file:
        dna_sequence = file.read().strip()
    
    print(f"🧬 DNA sequence length: {len(dna_sequence)} bases")

    # Get list of STRs from database header (all columns except 'name')
    str_list = list(database[0].keys())[1:]
    print(f"🔍 Analyzing STRs: {', '.join(str_list)}")

    # Calculate longest run for each STR
    str_counts = {}
    for str_seq in str_list:
        count = longest_match(dna_sequence, str_seq)
        str_counts[str_seq] = count
        print(f"   {str_seq}: {count} repeats")

    print("\n📋 Comparing with database:")

    # Check database for matching profile
    for person in database:
        match = True
        print(f"   {person['name']}: ", end="")
        
        for str_seq in str_list:
            if person[str_seq] != str_counts[str_seq]:
                match = False
                print(f"❌ {str_seq}({person[str_seq]} vs {str_counts[str_seq]}) ", end="")
                break
        
        if match:
            print("✅ FULL MATCH!")
            print(f"\n🎉 Match found: {person['name']}")
            return
        else:
            print("❌ No match")

    # No match found
    print("\n❌ No matching individual found in database")
    return


def longest_match(sequence, subsequence):
    """
    Returns length of longest run of subsequence in sequence.
    """
    longest_run = 0
    sub_length = len(subsequence)
    seq_length = len(sequence)

    # Check each possible starting position
    for i in range(seq_length):
        count = 0
        
        # Keep checking consecutive matches
        while True:
            start = i + count * sub_length
            end = start + sub_length
            
            if start + sub_length > seq_length:
                break
                
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        
        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()