# Transformer-based sequence alignment
This project was my master thesis at the Faculty of Electrical Engineering and Computing in Zagreb. It connects the areas of machine learning, natural language processing, and bioinformatics and deals with the use of transformer models for pairwise protein sequence alignment. Complete paper written in Croatian can be found in the repository.

## Project overview
### Protein sequence alignment
Proteins consist of a large number of amino acids. Each amino acid (there are 20 different amino acids in total) is represented by one letter, or symbol. Proteins in bioinformatics are therefore viewed as large strings consisting of 20 possible capital letters. To compare two (or more) protein sequences (e.g., to determine regions of similarity, predict functional and structural similarities, or determine an evolutionary relationship), they need to be aligned. Aligning two or more sequences means inserting gap characters (gap character is "-") at appropriate positions in the sequences to achieve as many matches as possible.
For example, the aligment of these two protein sequences:

V D R M R I R T W K V

Q D R R I N T W K S L V

is represented by the following two sequences:

V D R M R I R T W K - - V

Q D R - R I N T W K S L V

Pairwise alignment means aligning two sequences, while multiple sequence alignment, which is a more complex task, means aligning three or more sequences. This project deals with pairwise alignment of protein sequences.

## Repository and Usage
