import math
import matplotlib.pyplot as plt
import numpy as np
import rbo
from doc_utils import DocUtils
from typing import List

class VDBRBOScorer(DocUtils):
    @property
    def rbo_score_mapping(self):
        return {
            0.0: "The results are nothing alike.",
            0.1: "The results are nothing alike.",
            0.2: "The results are nothing alike.",
            0.3: "The results are somewhat alike.",
            0.4: "The results are somewhat alike.",
            0.5: "The results are somewhat alike.",
            0.6: "The results are somewhat alike.",
            0.7: "The results are quite alike.",
            0.8: "The results are quite alike.",
            0.9: "The results are very alike.",
            1: "The results are exactly the same.",
        }

    def round_up(self, n, decimals=1):
        multiplier = 10 ** decimals
        return round(math.ceil(n * multiplier) / multiplier, 2)

    def get_rbo_score(self, p=1):
        """
            Return the RBO score for Search Rankings
        """
        ranked_list_1_ids = self.get_field_across_documents('_id', self.ranked_list_1)
        ranked_list_2_ids = self.get_field_across_documents('_id', self.ranked_list_2)
        # TODO: Discuss RBO implementation - Should be it be a requirement?
        score = self.calculate_rbo_score(ranked_list_1_ids, ranked_list_2_ids, p=p)
        return score, self.rbo_score_mapping[self.round_up(score, 1)]
    
    def score_rbo(self, list_1, list_2, p=1):
        score = self.calculate_rbo_score(list_1, list_2, p=p)
        return score, self.rbo_score_mapping[self.round_up(score, 1)]

    def calculate_rbo_score(self, list_1, list_2, p=1):
        return rbo.RankingSimilarity(list_1, list_2).rbo(p=p)

    def get_rbo_heatmap_values(self, results_list, p=1, annotated=False, alias: List[str]=None):
        """An alias is useful if you want to name the results lists. Otherwise, it simply returns
        "ranked_list_1", "ranked_list_2" and so on"
        """
        if not annotated:
            rbo_scores = []
            results_list_dict = {}
            for i, r in enumerate(results_list):
                results_list_dict[f'results_list_{i + 1}'] = self.get_field_across_documents('_id', r)
            for r in results_list_dict.values():
                _rbo_score = []
                for r_2 in results_list_dict.values():
                    _rbo_score.append(self.calculate_rbo_score(r, r_2, p=p))
                rbo_scores.append(_rbo_score)
            return rbo_scores

        rbo_scores = {}
        results_list_dict = {}
        # Retrieve the document ID to get list
        if alias is None:
            alias = [f'results_{i+1}' for i in range(len(results_list))]
        for i, r in enumerate(results_list):
            results_list_dict[f'results_list_{i + 1}'] = self.get_field_across_documents('_id', r)
        for i, results_list in enumerate(results_list_dict.values()):
            _rbo_score = {}
            for j, results_list_2 in enumerate(results_list_dict.values()):
                _rbo_score[alias[j]] = self.calculate_rbo_score(results_list, results_list_2, p=p)
            rbo_scores[alias[i]] = _rbo_score
        return rbo_scores

    def rbo_heatmap(self, results_list, x_labels=[], y_labels=[], title="RBO Heatmap", p=1):
        """
        Provide a heatmap using RBO
        results_list is a list of results lists. They must have their _id fields intact.
        """
        results_values = self.get_rbo_heatmap_values(results_list, p=p)
        fig, ax = plt.subplots()
        im = ax.imshow(results_values)
        ax.set_xticks(np.arange(len(x_labels)))
        ax.set_yticks(np.arange(len(y_labels)))
        ax.set_xticklabels(x_labels)
        ax.set_yticklabels(y_labels)
        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        for i in range(len(x_labels)):
            for j in range(len(y_labels)):
                text = ax.text(j, i, results_values[i, j],
                            ha="center", va="center", color="w")
        ax.set_title(title)
        plt.show()
