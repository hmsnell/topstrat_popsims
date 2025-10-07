'''
Reference: Scott McCallum 
Simulation of a selective sweep by a single beneficial mutation using the Out of Africa 3 population demographic
https://popsim-consortium.github.io/stdpopsim-docs/stable/catalog.html#sec_catalog_homsap_models_outofafrica_3g09
'''
# sloppy, but the 'warnings' module ignores a couple future warnings in stdpopsim
import warnings
#import pandas as pd
warnings.filterwarnings("ignore")
import stdpopsim
#import matplotlib.pyplot as plt
import numpy as np
import time
import sys

sim_number = sys.argv[1]

start = time.time()

true_seed = int(sim_number) + 12345

species = stdpopsim.get_species("HomSap")  # Homo sapiens
model = species.get_demographic_model("OutOfAfrica_3G09")
samples = {"YRI": 1000, "CEU": 1000, "CHB": 1000}

contig = species.get_contig(length=1e6)

'''
The next session will provide settings for the sweep. This includes:
 - randomly selecting a chromosome in a population of our choice
 - The position will be specific within the contig
'''

locus_id = "hard_sweep"
coordinate = round(contig.length / 2)  # this is where the sweep will be located
print(coordinate)
contig.add_single_site(
    id=locus_id,
    coordinate=coordinate
)

'''
Now we run the simulation using SLiM. For comparison a neutral simulation will 
also be run

slim_scaling_factor:
    Reduces population size by a scaling factor (Q) 
    Rescales time by Q 
    If model selection is used it would rescale the selection coefficient by Q 
    In general, this results in indistinguishable output. However, this may NOT be true in simulations with large 
    amount of selection. In my case, I'm assuming we do not have "large" amounts of selection since there is on a single 
    selective sweep. 
    Link --> https://popsim-consortium.github.io/stdpopsim-docs/stable/tutorial.html#slim-scaling-factor 
    
slim_burn_in:
    Number of generations before SLiM kicks in. 
    MSPRIME is used for the prior generations 
    The value of 10 is the default and considered to be "safe" 
    Link --> https://popsim-consortium.github.io/stdpopsim-docs/stable/tutorial.html#the-slim-burn-in 
    
min_freq_at_end 
    Frequency of the mutation in the present data (e.g., at the end of the sweep) should be greater than this value.  
    Link --> https://popsim-consortium.github.io/stdpopsim-docs/stable/tutorial.html#selective-sweeps 
    (scroll down to min_freq_at_end) 
'''

engine = stdpopsim.get_engine("slim")

ts_neutral = engine.simulate(
    model,
    contig,
    samples,
    seed=true_seed,
    # no extended events
    slim_burn_in=10  # number of gens before SLiM begins (these gens are msprime). 10 is safe and default
)

with open("neutral_simulation_"+sim_number, "w") as vcf_file:
    ts_neutral.write_vcf(vcf_file)

end = time.time()
delta = round((end - start) / 60, 2)
print(delta, " minutes")