 echo [$(date)]: "START"
 echo [$(date)]: "creating environment"
 conda create --prefix ./env python=3.8 -y
 echo [$(date)]: "activate environment"
 source activate ./env
 echo [$(date)]: "install pywin32"
 conda install -c anaconda pywin32 -y
 echo [$(date)]: "install requirements"
 pip install -r requirements.txt
 echo [$(date)]: "export conda environment"
 conda env export > conda.yaml
 echo [$(date)]: "initialize git repository"
 git init
 echo [$(date)]: "add env to gitignore"
 echo "env/" > .gitignore
 pip install - e . # Added by Ketan Gangal
 # echo "# ${PWD}" > README.md
 echo [$(date)]: "first commit"
 git add .
 git commit -m "first commit"
 echo [$(date)]: "END"

#echo [$(date)]: "make neccesary dirs"
#mkdir -p src/utils \
#src/aws_configurations \
#src/aws_infrastructure \
#src/aws_infrastructure_control \
#src/aws_production_control
#
#
#echo [$(date)]: "make aws model training file"
#touch src/__init__.py \
#src/aws_model_training.py
#
#echo [$(date)]: "make util files"
#touch src/utils/__init__.py \
#src/utils/common.py \
#src/utils/sagemaker_utils.py
#
#echo [$(date)]: "make aws production control files"
#touch src/aws_production_control/__init__.py \
#src/aws_production_control/delete_endpoint.py \
#src/aws_production_control/deploy_aws_sagemaker.py \
#src/aws_production_control/prediction.py \
#src/aws_production_control/switch_models.py
#
#echo [$(date)]: "make aws infra control files"
#touch src/aws_infrastructure_control/__init__.py \
#src/aws_infrastructure_control/aws_infrastructure_setup.py \
#src/aws_infrastructure_control/aws_infrastructure_destroy.py
#
#echo [$(date)]: "make aws infra setup files"
#touch src/aws_infrastructure/__init__.py \
#src/aws_infrastructure/main.tf \
#src/aws_infrastructure/variable.tf
#
#echo [$(date)]: "make aws config files"
#touch src/aws_configurations/__init__.py \
#src/aws_configurations/aws_config.yaml
#
#echo [$(date)]: "base template created"
#git add .
#git commit -m "base template created"
#echo [$(date)]: "END"
