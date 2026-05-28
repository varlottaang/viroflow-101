#!/usr/bin/env python3
# fasta_summary.py
# A beginner-friendly script to summarize a viral FASTA file

import sys
import os

def validate_input(fasta_file):
    """Validate that the input file exists and is readable."""
    if not os.path.exists(fasta_file):
        print(f"Error: File {fasta_file} not found", file=sys.stderr)
        sys.exit(1)
    
    if not os.access(fasta_file, os.R_OK):
        print(f"Error: File {fasta_file} is not readable", file=sys.stderr)
        sys.exit(1)

def parse_fasta(fasta_file):
    """Parse FASTA file and return sequence name and sequence."""
    sequence_name = ""
    sequence = ""
    
    with open(fasta_file, "r") as file:
        for line in file:
            line = line.strip()
            
            if not line:  # Skip empty lines
                continue
            
            if line.startswith(">"):
                sequence_name = line[1:]
            else:
                sequence += line.upper()
    
    return sequence_name, sequence

def calculate_statistics(sequence):
    """Calculate nucleotide statistics."""
    length = len(sequence)
    
    if length == 0:
        print("Error: No sequence found in FASTA file", file=sys.stderr)
        sys.exit(1)
    
    a_count = sequence.count("A")
    t_count = sequence.count("T")
    g_count = sequence.count("G")
    c_count = sequence.count("C")
    other_count = length - (a_count + t_count + g_count + c_count)
    
    gc_content = ((g_count + c_count) / length) * 100
    
    return {
        "length": length,
        "a_count": a_count,
        "t_count": t_count,
        "g_count": g_count,
        "c_count": c_count,
        "other_count": other_count,
        "gc_content": gc_content
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: fasta_summary.py <fasta_file>", file=sys.stderr)
        sys.exit(1)
    
    fasta_file = sys.argv[1]
    
    # Validate input
    validate_input(fasta_file)
    
    # Parse FASTA
    sequence_name, sequence = parse_fasta(fasta_file)
    
    # Calculate statistics
    stats = calculate_statistics(sequence)
    
    # Print results
    print("Genome summary")
    print("-" * 30)
    print(f"Sequence name: {sequence_name}")
    print(f"Genome length: {stats['length']} nucleotides")
    print(f"A count: {stats['a_count']}")
    print(f"T count: {stats['t_count']}")
    print(f"G count: {stats['g_count']}")
    print(f"C count: {stats['c_count']}")
    print(f"Other/ambiguous: {stats['other_count']}")
    print(f"GC content: {stats['gc_content']:.2f}%")

if __name__ == "__main__":
    main()
