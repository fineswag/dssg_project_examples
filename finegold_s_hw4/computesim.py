import numpy as np
import math

from mrjob.job import MRJob
from itertools import combinations, permutations

from scipy.stats.stats import pearsonr

# collaborated with Mark Grozen-Smith

class RestaurantSimilarities(MRJob):

    def steps(self):
        "the steps in the map-reduce process"
        thesteps = [
            self.mr(mapper=self.line_mapper, reducer=self.users_items_collector),
            self.mr(mapper=self.pair_items_mapper, reducer=self.calc_sim_collector)
        ]
        return thesteps

    def line_mapper(self,_,line):
        "this is the complete implementation"
        user_id,business_id,stars,business_avg,user_avg=line.split(',')
        yield user_id, (business_id,stars,business_avg,user_avg)
        
    def users_items_collector(self, user_id, values):
        """
        #iterate over the list of tuples yielded in the previous mapper
        #and append them to an array of rating information
        """
        
        yield user_id, list(values)
                
    def pair_items_mapper(self, user_id, values):
        """
        ignoring the user_id key, take all combinations of business pairs
        and yield as key the pair id, and as value the pair rating information
        """
	    
	    # choose two rows and get the values
        for val_1 in values:
            for val_2 in values:        
                if val_1[0] < val_2[0]:
                    yield (val_1[0],val_2[0]), (val_1[1], val_2[1], val_1[2], val_2[2], val_1[3], val_2[3])

    def calc_sim_collector(self, key, values):
        """
        Pick up the information from the previous yield as shown. Compute
        the pearson correlation and yield the final information as in the
        last line here.
        """
        
        # mimic pearson calculation in the code
        values = list(values)
        n_common = len(values)
        if n_common == 0:
            rho = 0
        else:         
            diff1=[float(val[0])-float(val[4]) for val in values]
            diff2=[float(val[1])-float(val[5]) for val in values]
            rho=pearsonr(diff1, diff2)[0]
        
        if math.isnan(rho) == True: rho = 0
        
        yield key, (rho, n_common)
        

#Below MUST be there for things to work
if __name__ == '__main__':
    RestaurantSimilarities.run()
