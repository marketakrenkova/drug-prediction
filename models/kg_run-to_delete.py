#!/usr/bin/python3

import pandas as pd
import time
import os.path
import sys

import torch

from pykeen.models import predict
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from pykeen.models import TransE, NodePiece
from pykeen.evaluation import RankBasedEvaluator


def convert_to_triples_factory(data):
    tf_data = TriplesFactory.from_labeled_triples(
      data[["head", "relation", "tail"]].values,
      create_inverse_triples=True,
      entity_to_id=None,
      relation_to_id=None,
      compact_id=False 
    )

    return tf_data

def train_model(model, tf_train, tf_valid, tf_test, detail): 
    # creating a model
    if model == 'NodePiece':  # TODO: make it work
        result = pipeline(
            training = tf_train,
            testing = tf_test,
            validation = tf_valid,
            model = NodePiece,
            model_kwargs = dict(
                    tokenizers = ['anchor', 'relation'],
                    num_tokens = [20, 12],
                    tokenizers_kwargs = [
                        dict(
                            selection = "MixtureAnchorSelection",
                            selection_kwargs=dict(
                            selections=["degree", "pagerank", "random"],
                            ratios=[0.4, 0.4, 0.2],
                            num_anchors=4000
                            ),
                        searcher = "ScipySparse",
                        ),
                        dict(),
                    ],
                    embedding_dim = 64,
                    interaction = 'rotate'
                ),
            device = 'gpu',
            training_kwargs = dict(
                num_epochs = 20,
                checkpoint_name = model + '_checkpoint.pt',
                ckeckpoint_directory = 'kg_checkpoints',
                checkpoint_frequency = 10
            )
        )
    else:    
        result = pipeline(
            training = tf_train,
            testing = tf_test,
            validation = tf_valid,
            model = model,
            optimizer = 'Adam',
            evaluator = RankBasedEvaluator,
            epochs = 20,
            device = 'gpu',
            training_kwargs = dict(
                num_epochs = 20,
                checkpoint_name = model + '-' + detail + '_checkpoint.pt',
                checkpoint_directory = 'kg_checkpoints',
                checkpoint_frequency = 10
            ),
            #stopper='early',
            #stopper_kwargs=dict(frequency=5, patience=2, relative_delta=0.002),
        )
    return result

def get_predictions(result, model_name, detail):
    predictions_dir = 'predictions/'
    
    predicted_tails_df = predict.get_head_prediction_df(
        model = result.model, 
        tail_label = "Leuprolide", 
        relation_label = "decrease_adverse_effects", 
        triples_factory = result.training,
    )
    print('Leuprolide - decrease_adverse_effects:')
    print(predicted_tails_df.head(20))
    predicted_tails_df = predicted_tails_df.head(100)
    predicted_tails_df.to_csv(predictions_dir + model_name + '-Leuprolide-predictions-' + detail + '.csv')

    predicted_df_2 = predict.get_head_prediction_df(
        model = result.model, 
        tail_label = "Galantamine", 
        relation_label = "increase_congestive_heart_failure", 
        triples_factory = result.training,
    )
    print('Galantamine - increase_congestive_heart_failure')
    print(predicted_df_2.head(20))
    predicted_df_2 = predicted_df_2.head(100)
    predicted_df_2.to_csv(predictions_dir + model_name + '-galantamine-predictions-'+ detail +'.csv')
    
    predicted_df_3 = predict.get_tail_prediction_df(
        model = result.model, 
        head_label = "Pineapple", 
        relation_label = "interacts_with", 
        triples_factory = result.training,
    )
    print('Pineapple - interacts_with')
    print(predicted_df_3.head(20))
    predicted_df_3 = predicted_df_3.head(100)
    predicted_df_3.to_csv(predictions_dir + model_name + '-pineapple-predictions-'+ detail +'.csv')

    predicted_df_4 = predict.get_tail_prediction_df(
        model = result.model, 
        head_label = "Vedolizumab", 
        relation_label = "increase_infection", 
        triples_factory = result.training,   
    )
    print('Vedolizumab - increase_infection')
    print(predicted_df_4.head(20))
    predicted_df_4 = predicted_df_4.head(100)
    predicted_df_4.to_csv(predictions_dir + model_name + '-vedolizumab-predictions-' + detail + '.csv')
    
    #predicted_all_df = predict.get_all_prediction_df(
    #    model = result.model, 
    #    k = 200,
    #    triples_factory = result.training,
    #)

    #print(predicted_all_df.head(20)) 
    #predicted_all_df.to_csv(model_name + '-all_predicitons.csv')

    

def main(detail):

    model_name = 'HolE'
    trained_model = 'results-' + model_name + '/trained_model.pkl'

    # TODO: 
    # if os.path.isfile(trained_model):
    #     print('Loading trained model...')
    #     results = torch.load(trained_model)
    #     print(results.model)
    # else:

    print('Reading data...')
    train = pd.read_csv('data/triplets/train.tsv', sep='\t', index_col=[0], engine='python')
    valid = pd.read_csv('data/triplets/valid.tsv', sep='\t', index_col=[0], engine='python')
    test = pd.read_csv('data/triplets/test.tsv', sep='\t', index_col=[0], engine='python')

    print('Transforming...')
    tf_train = convert_to_triples_factory(train.astype(str))
    tf_valid = convert_to_triples_factory(valid.astype(str))
    tf_test = convert_to_triples_factory(test.astype(str))
    
    print('Training model...')
    start_time = time.time()
    results = train_model(model_name, tf_train, tf_valid, tf_test, detail)
    print('Training done.')
    print("--- %s seconds ---" % (time.time() - start_time))

    results.save_to_directory("results-" + model_name + '-' + detail)


    get_predictions(results, model_name, detail)

if __name__ == "__main__":
    detail = sys.argv[1]
    main(detail)    
    