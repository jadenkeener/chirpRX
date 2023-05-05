# chirpRX
2022 Chirpsounder receiver project in collaboration with Los Alamos National Labs

Welcome to ChirpRX! The goal of this system is to create a tool capable of 
automatically capturing and processing Ionosonde data into Ionograms.

A project overview and operational instructions can be found in the included 
report. (./report)

Please run the program from this folder. Moving any of the scripts 
may cause it to break! For example, open a terminal in this folder and run:

$ python3 timertrigger.py -H 10 -M 23 -S 3

Outputs from automatic capture will stored in ./RAW/ ./chirp/ and ./png/
Outputs from the timelapser.py script will be in this (root) folder. 
