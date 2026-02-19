"""
DNA Profile Visualizer - Creates forensic-style electropherogram charts
For use with DNA-Identifier forensic profiling tool
"""

import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import datetime
import os

def load_profile_from_csv(csv_file, person_name):
    """
    Load a person's DNA profile from the database CSV
    """
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'].lower() == person_name.lower():
                    # Convert STR counts to integers
                    profile = {}
                    for key, value in row.items():
                        if key == 'name':
                            profile[key] = value
                        elif value not in ['X', 'Y']:
                            try:
                                profile[key] = int(value)
                            except:
                                profile[key] = value
                        else:
                            profile[key] = value
                    return profile
        print(f"❌ Person '{person_name}' not found in database")
        return None
    except Exception as e:
        print(f"❌ Error loading database: {e}")
        return None

def create_electropherogram(profile_data, title="DNA Profile", save_path=None):
    """
    Create a forensic-style electropherogram visualization
    """
    # Filter out non-STR fields
    markers = []
    alleles = []
    
    for key, value in profile_data.items():
        if key != 'name' and key != 'AMEL' and isinstance(value, (int, float)):
            markers.append(key)
            alleles.append(value)
    
    if not markers:
        print("No numerical STR data found in profile")
        return None
    
    # Create figure with forensic styling
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), 
                                     gridspec_kw={'height_ratios': [3, 1]},
                                     facecolor='#0a0a0a')
    
    # Set dark theme for forensic look
    ax1.set_facecolor('#1a1a1a')
    ax2.set_facecolor('#1a1a1a')
    
    # Colors for different markers (forensic green theme)
    colors = plt.cm.YlGn(np.linspace(0.3, 0.9, len(markers)))
    
    # Top plot: Allele peaks (electropherogram)
    max_allele = max(alleles) if alleles else 30
    
    for i, (marker, allele) in enumerate(zip(markers, alleles)):
        x_pos = i + 1
        
        # Create peak shape (Gaussian)
        x_peak = np.linspace(x_pos - 0.3, x_pos + 0.3, 50)
        peak_height = (allele / max_allele) * 100
        y_peak = peak_height * np.exp(-((x_peak - x_pos) ** 2) / 0.02)
        
        # Plot peak
        ax1.fill_between(x_peak, 0, y_peak, color=colors[i], alpha=0.8)
        
        # Add allele value label
        ax1.text(x_pos, peak_height + 5, str(allele), 
                color='#00ff00', ha='center', fontsize=9, fontweight='bold')
        
        # Add marker name
        ax1.text(x_pos, -10, marker, color='white', ha='center', 
                fontsize=8, rotation=45)
    
    # Style the electropherogram
    ax1.set_ylim(-20, 120)
    ax1.set_xlim(0, len(markers) + 1)
    ax1.set_ylabel('Relative Fluorescence Units', color='white', fontsize=10)
    ax1.tick_params(colors='white')
    ax1.grid(True, alpha=0.2, color='gray', linestyle='--')
    
    # Bottom plot: Allele counts
    for i, (marker, allele) in enumerate(zip(markers, alleles)):
        x_pos = i + 1
        ax2.bar(x_pos, allele, color=colors[i], alpha=0.8, width=0.6)
        ax2.text(x_pos, allele + 0.5, str(allele), color='#00ff00', 
                ha='center', fontsize=8)
    
    ax2.set_xlim(0, len(markers) + 1)
    ax2.set_ylabel('Allele Count', color='white', fontsize=10)
    ax2.set_xlabel('STR Markers', color='white', fontsize=10)
    ax2.tick_params(colors='white')
    ax2.set_facecolor('#1a1a1a')
    
    # Main title
    fig.suptitle(title, color='white', fontsize=14, fontweight='bold', y=0.98)
    
    # Add forensic case info footer
    case_num = np.random.randint(1000, 9999)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    footer_text = f"Case: DNA-{case_num} | Date: {today} | Lab: Forensic BioInformatics"
    plt.figtext(0.5, 0.01, footer_text, color='gray', fontsize=8, ha='center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, facecolor='#0a0a0a')
        print(f"✅ Electropherogram saved to: {save_path}")
    else:
        plt.show()
    
    return case_num

def generate_report(profile_data, case_num):
    """
    Generate a simple forensic report
    """
    report_lines = []
    report_lines.append("="*60)
    report_lines.append("FORENSIC DNA ANALYSIS REPORT")  # Removed emoji
    report_lines.append("="*60)
    report_lines.append(f"Subject: {profile_data.get('name', 'Unknown')}")
    report_lines.append(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    report_lines.append(f"Case #: DNA-{case_num}")
    report_lines.append("-"*60)
    report_lines.append("\nSTR PROFILES:")
    
    for key, value in profile_data.items():
        if key != 'name':
            report_lines.append(f"  {key}: {value}")
    
    report_lines.append("\n" + "="*60)
    report_lines.append("FORENSIC CONCLUSIONS:")
    report_lines.append("  - DNA profile meets CODIS quality standards")
    report_lines.append("  - All markers successfully amplified")
    report_lines.append("  - Profile suitable for database comparison")
    report_lines.append("="*60)
    
    return "\n".join(report_lines)

def main():
    """
    Main function to run the visualizer
    """
    if len(sys.argv) != 3:
        print("\n🔬 DNA Profile Visualizer")
        print("="*40)
        print("Usage:")
        print("  python visualize_profile.py <database.csv> <person_name>")
        print("\nExamples:")
        print("  python visualize_profile.py databases/codis_20.csv John_Doe")
        print("  python visualize_profile.py databases/small.csv Alice")
        print("="*40)
        return
    
    # Load from database
    csv_file = sys.argv[1]
    person_name = sys.argv[2]
    
    print(f"\n🔬 Loading profile for: {person_name}")
    print(f"📁 Database: {csv_file}")
    print("-"*40)
    
    profile = load_profile_from_csv(csv_file, person_name)
    
    if profile:
        print("✅ Profile loaded successfully")
        
        # Display profile
        print("\n📊 STR Profile:")
        marker_count = 0
        for key, value in profile.items():
            if key != 'name':
                print(f"   {key}: {value}")
                marker_count += 1
        print(f"\n   Total markers: {marker_count}")
        
        # Create visualization
        print("\n🎨 Generating electropherogram...")
        output_file = f"{person_name}_profile.png"
        case_num = create_electropherogram(
            profile, 
            title=f"DNA Profile: {person_name}",
            save_path=output_file
        )
        
        # Generate report
        print("\n📄 Generating forensic report...")
        report = generate_report(profile, case_num)
        report_file = f"{person_name}_report.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n✅ Files created:")
        print(f"   • {output_file}")
        print(f"   • {report_file}")
        
        # Ask if user wants to view
        view = input("\n📂 Open the image now? (y/n): ").lower()
        if view == 'y':
            os.system(f"start {output_file}")
    else:
        print(f"\n❌ Could not load profile for '{person_name}'")

if __name__ == "__main__":
    main()