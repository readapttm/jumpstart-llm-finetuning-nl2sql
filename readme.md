# Finetune a simple LLM in AWS Jumpstart

This notebook demostrates a simple application of finetuning an LLM to translate natural language questions into SQL. We will train on the BIRD dataset (available here: https://bird-bench.github.io/). The goal is to see if finetuning leads to an appreciable improvement is SQL writing ability for a model with few paramters, in this case llama 3.2 1B Instruct. In brief, in the 3 provided notebooks we will:

- get the BIRD data
- reformat as compact prompts
- save prompts to S3
- finetune the model
- save model artifacts to S3
- deploy base and finetuned models
- test their comparative SQL writing ability
- delete deployments (to avoid long term hosting costs)

For the parameters provided in these notebooks, the entire project should cost <$10 (provided the endpoints are torn down immediately after inference concludes). 


Note, Jumpstart expects data stored in S3. If you don't have an AWS account then you will need to set one up and activate S3 and sagemaker. 


## AWS Set-up

### Authentication 
These notebooks establish a connection to AWS via SSO. If you are using the same method, save your profile in the form aws_profile='{Role}-{AccountNumber}' e.g. 'AWSAccess-123456789012'  in a .env file in the same folder as the notebooks. If you are authenticating via a different method some adjustments to the scripts may be required.

### Sagemaker
To configure sagemaker you will need to create a role that can access both SageMaker and S3 (so that your model artifacts can be saved). To do this, go to the IAM section in your AWS account, on the left tab under Access management/Roles; create a role named AmazonSageMakerFullAccessRole and attach the following policies: AmazonS3FullAccess, AmazonSageMakerFullAccess and a custom inline policy - name it sagemaker_iam_get_role and add the following statement (replacing the value of {YourAWSAccountNumber} as appropriate):

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": "iam:GetRole",
            "Resource": "arn:aws:iam::{YourAWSAccountNumber}:role/AmazonSageMakerFullAccessRole"
        }
    ]
}
```

You may also want to set up Sagemaker Unified Studio for convenience.


## Instructions (once you have configured AWS as per the above)
0) First download the data (both train.zip and dev.zip) and save locally in a folder named BIRD.
1) Run 1_prep_BIRD.ipynb
     - update the global variables 'drive_loc' (to point at the parent directory of your BIRD folder) and 'bucket_name' to set the name of your S3 bucket
     - Run each cell
     - This script will load the queries, questions and table descriptions and reformat in a human readable way, then save to disk
     - The model we will be using on Jumpstart has relatively low token limits so we need to make the prompts as short as possible

2) Run 2_fine_tuning.py
     - Update the parameters train_data_location and valid_data_location
     - Update the default training hyperparameters if desired
     - Run each cell

3) Run 3_deploy_and_test.py
     - Inspect S3 to determine where your new model has been saved by the sagemaker role; update the values of s3_bucket and bucket_prefix as required
     - Ensure the 'folder' parameter points at the location of the test data file (bird_test_abrev.jsonl) you created in step 1.
     - results_to_test is set to 20 to avoid running many inference calls but update as desired
     - Run each cell (apart from the final delete_predictor cell unless you have finished using your endpoint)
     - Be sure to run the final cell (predictor.delete_predictor()) once you are finished to avoid unwanted deployement costs for the base and finetuned models



If you get stuck at any point (such as account authentication issues) or require more information please check the below documentation 

-  "Deploy a pre-trained model using the SageMaker Model class":  https://sagemaker.readthedocs.io/en/v2.163.0/overview.html
- https://sagemaker-examples.readthedocs.io/en/latest/introduction_to_amazon_algorithms/jumpstart-foundation-models/llama-2-finetuning.html
- https://aws.amazon.com/blogs/machine-learning/llama-3-2-models-from-meta-are-now-available-in-amazon-sagemaker-jumpstart/

NB. All code in this repository is provided for educational purposes only, with absolutely no warranty explicit, implied, or otherwise.