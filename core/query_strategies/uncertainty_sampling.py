import numpy as np 
import torch

class UncertaintySamplingStrategy():
    def __init__(self,dm,clf,conf,logger):
        self.dm       = dm 
        self.clf      = clf 
        self.conf     = conf 
        self.logger   = logger 
        pass 
    
    def query_points(self,batch_size,inf_out=None):
        cur_unlbld_idcs  = self.dm.get_current_unlabeled_idcs()
        cur_unlbld_ds    = self.dm.get_subset_dataset(cur_unlbld_idcs)

        if(inf_out is None):
            self.logger.debug('running infernce')
            inf_out = self.clf.predict(cur_unlbld_ds, self.conf['inference_conf']) 
        
        confidence_scores = inf_out['probs']
        if type(confidence_scores) == np.ndarray or type(confidence_scores) == list:    
            probs = torch.Tensor(np.array(confidence_scores))
        else:
            probs = confidence_scores
        
        sample_size     = min(batch_size, len(probs))
        idx             = np.argsort(probs)[:sample_size]

        selected_idcs   = np.array(cur_unlbld_idcs)[idx.numpy()]

        return selected_idcs
