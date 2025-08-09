#!/usr/bin/env python

import os
import subprocess

def convert_md_to_html(md_file_path, output_dir=None):
    """
    Converts a Markdown file to HTML using pandoc.
    """
    html_file_path = os.path.splitext(md_file_path)[0] + ".html"
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        html_file_path = os.path.join(output_dir, os.path.basename(html_file_path))
    
    try:
        subprocess.run(['pandoc', md_file_path, '-o', html_file_path], check=True)
        print(f"Converted: {md_file_path} -> {html_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {md_file_path}: {e}")

def recursively_convert_md_to_html(start_dir, output_dir=None):
    """
    Recursively traverses directories starting from `start_dir`,
    converting all .md files to .html.
    """
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.lower().endswith('.md'):
                md_file_path = os.path.join(root, file)
                convert_md_to_html(md_file_path, output_dir)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Recursively convert .md files to .html using pandoc.")
    parser.add_argument("start_dir", help="The starting directory to search for .md files.")
    parser.add_argument("--output-dir", help="Optional output directory for HTML files. Defaults to same as input.", default=None)

    args = parser.parse_args()
    recursively_convert_md_to_html(args.start_dir, args.output_dir)
