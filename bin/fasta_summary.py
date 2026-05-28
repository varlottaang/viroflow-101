#!/usr/bin/env python3
# fasta_summary.py
# A beginner-friendly script to summarize a viral FASTA file

import sys
import os
import json
import csv
from argparse import ArgumentParser

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

def output_txt(sequence_name, stats):
    """Output results in plain text format."""
    output = []
    output.append("Genome summary")
    output.append("-" * 30)
    output.append(f"Sequence name: {sequence_name}")
    output.append(f"Genome length: {stats['length']} nucleotides")
    output.append(f"A count: {stats['a_count']}")
    output.append(f"T count: {stats['t_count']}")
    output.append(f"G count: {stats['g_count']}")
    output.append(f"C count: {stats['c_count']}")
    output.append(f"Other/ambiguous: {stats['other_count']}")
    output.append(f"GC content: {stats['gc_content']:.2f}%")
    return "\n".join(output)

def output_json(sequence_name, stats):
    """Output results in JSON format."""
    data = {
        "sequence_name": sequence_name,
        "genome_length": stats['length'],
        "nucleotide_counts": {
            "A": stats['a_count'],
            "T": stats['t_count'],
            "G": stats['g_count'],
            "C": stats['c_count'],
            "other": stats['other_count']
        },
        "gc_content_percent": round(stats['gc_content'], 2)
    }
    return json.dumps(data, indent=2)

def output_csv(sequence_name, stats):
    """Output results in CSV format."""
    output = []
    output.append("Metric,Value")
    output.append(f"Sequence name,{sequence_name}")
    output.append(f"Genome length,{stats['length']}")
    output.append(f"A count,{stats['a_count']}")
    output.append(f"T count,{stats['t_count']}")
    output.append(f"G count,{stats['g_count']}")
    output.append(f"C count,{stats['c_count']}")
    output.append(f"Other/ambiguous,{stats['other_count']}")
    output.append(f"GC content (%),{stats['gc_content']:.2f}")
    return "\n".join(output)

def main():
    parser = ArgumentParser(description="Summarize a viral FASTA file")
    parser.add_argument("fasta_file", help="Path to FASTA file")
    parser.add_argument("--format", default="txt", choices=["txt", "json", "csv", "all"],
                        help="Output format (default: txt)")
    
    args = parser.parse_args()
    
    # Validate input
    validate_input(args.fasta_file)
    
    # Parse FASTA
    sequence_name, sequence = parse_fasta(args.fasta_file)
    
    # Calculate statistics
    stats = calculate_statistics(sequence)
    
    # Generate output based on format
    if args.format == "txt" or args.format == "all":
        print(output_txt(sequence_name, stats))
    
    if args.format == "json":
        print(output_json(sequence_name, stats))
    elif args.format == "all":
        print("\n" + "="*30 + "\n")
        print(output_json(sequence_name, stats))
    
    if args.format == "csv":
        print(output_csv(sequence_name, stats))
    elif args.format == "all":
        print("\n" + "="*30 + "\n")
        print(output_csv(sequence_name, stats))

if __name__ == "__main__":
    main()
