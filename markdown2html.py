#!/usr/bin/python3
''' define function that conver html to markdown'''


if __name__ == '__main__':
  import sys
  import os
  import re

  def convert_heading_tohtml(line):
    """Converts a Markdown heading line to HTML."""

    count_hashes = line.count("#")
    if 1 <= count_hashes <= 6:
      return f"<h{count_hashes}>{line[count_hashes:].strip()}</h{count_hashes}>"
    else:
      return line


  def convert_list_tohtml(line, list_type):
    """Converts a Markdown list item line to HTML ."""

    if line.startswith(list_type[0]):  
      return f"<li>{line[2:].strip()}</li>" 
    else:
      return line


  def convert_paragraph_tohtml(lines):
    """Converts a sequence of Markdown lines to HTML paragraphs."""

    paragraph = ""
    for line in lines:
      paragraph += line.rstrip() + " "
    paragraph = paragraph.rstrip()

    if paragraph:
      paragraph = convert_inline_element_tohtml(paragraph, "<b>", "</b>")
      return "<p>" + paragraph.replace("\n\n", "</p>\n<p>") + "</p>\n"
    else:
      return ""


  def convert_inline_element_tohtml(text, opening_tag, closing_tag):
    """Converts inline Markdown formatting to HTML."""
  
    pattern = f"{opening_tag}(.*?){closing_tag}"
    return re.sub(pattern, rf"\1", text)


  def main():
    """Converts a Markdown file to HTML.

    Expects two arguments:
      1. Input Markdown file path.
      2. Output HTML file path.

    Prints error messages and exits with appropriate codes:
    """

    if len(sys.argv) < 3:
      print("Usage: ./markdown2html.py README.md README.html")
      exit(1)

    markdown_file = sys.argv[1]
    to_html = sys.argv[2]

    if not os.path.exists(markdown_file):
      print(f"Missing {markdown_file}")
      exit(1)

    with open(markdown_file, 'r') as md_f, open(to_html, 'w') as html_f:
      current_paragraph = []
      in_list = None
      for line in md_f:
        if line.startswith("#"):
          if current_paragraph:
            html_f.write(convert_paragraph_tohtml(current_paragraph))
            current_paragraph = []
          html_f.write(convert_heading_tohtml(line))
        elif line.startswith("-"):
          if in_list != "-":
            if in_list:
              html_f.write("</ol>\n")
            in_list = "-"
            html_f.write("<ul>\n")
          html_f.write(convert_list_tohtml(line, in_list))
        elif line.startswith("*"):
          if in_list != "*":
            if in_list:
              html_f.write("</ul>\n")
            in_list = "*"
            html_f.write("<ol>\n")
          html_f.write(convert_list_tohtml(line, in_list))
        else:
          if in_list:
            if in_list == "ul":
              html_f.write("</ul>\n")
            else:
              html_f.write("</ol>\n")
            in_list = None
          current_paragraph.append(line)
      if in_list:
          if in_list == "ul":
              html_f.write("</ul>\n")
          else:
              html_f.write("</ol>\n")
      if current_paragraph:
        html_f.write(convert_paragraph_tohtml(current_paragraph))

  
  main()