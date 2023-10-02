# Transformer-based sequence alignment
This project was my master thesis at the Faculty of Electrical Engineering and Computing in Zagreb. It connects the areas of machine learning, natural language processing, and bioinformatics and deals with the use of transformer models for pairwise protein sequence alignment. Complete thesis written in Croatian can be found in the repository. The idea for the thesis came from a paper that was published in early 2023 (Dotan et al., Multiple sequence alignment as a sequence-to-sequence learning problem).

## Project Overview
### Protein Sequence Alignment
Proteins consist of a large number of amino acids. Each amino acid (there are 20 different amino acids in total) is represented by one letter, or symbol. Proteins in bioinformatics are therefore viewed as large strings consisting of 20 possible capital letters. To compare two (or more) protein sequences (e.g., to determine regions of similarity, predict functional and structural similarities, or determine an evolutionary relationship), they need to be aligned. Aligning two or more sequences means inserting gap characters (gap character is "-") at appropriate positions in the sequences to achieve as many matches as possible.
For example, the alignment of these two protein sequences:

V D R M R I R T W K V

Q D R R I N T W K S L V

is represented by the following two sequences:

V D R M R I R T W K - - V

Q D R - R I N T W K S L V

Pairwise alignment means aligning two sequences, while multiple sequence alignment, which is a more complex task, means aligning three or more sequences. This project deals with pairwise alignment of protein sequences. There are many computational algorithms based on dynamic programming that have been applied to the sequence alignment problem. These algorithms produce optimal alignments but suffer from large time and space complexities when dealing with longer sequences. Other algorithms use different heuristics to speed up the process and therefore may not produce optimal alignments. Considering that biological sequences share many similarities with natural language, there is a strong assumption that deep learning algorithms that perform well on natural language tasks could also perform well on sequence alignment problem. An example of such an algorithm is the transformer.

### Transformer Architecture
The transformer architecture was first introduced in 2017 and proved to be very efficient at many different natural language processing tasks. Recently, it has also been used to solve different problems in bioinformatics. The picture below was taken from the paper that first introduced the transformer (Vaswani et al., Attention is all you need). It shows the main elements and layers of a transformer model (input embedding layer, encoder layer, decoder layer).

![image](https://github.com/ivanfurac/Transformer-Sequence-Alignment/assets/73389887/83181a1c-40d3-4d95-a58b-f50bbd76e498)

### Implementation and Dataset




## Repository and Usage
