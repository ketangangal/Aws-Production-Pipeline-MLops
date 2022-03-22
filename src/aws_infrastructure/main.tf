provider "aws" {
  access_key= var.access_key
  secret_key= var.secret_key
  region = var.region
}

# Aws Security Group For Mysql
resource "aws_security_group" "security_group" {
  name        = var.security_group
  description = "Allow All Traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "mlops-mysql-security-group"
  }
}

# Sagemaker Role Creation
resource "aws_iam_role" "sagemaker_role_name" {
  name = var.sagemaker_role_name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "sagemaker.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "policy" {
  name        = var.sagemaker_policy_name
  description = "A sagemaker policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:CreateBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "*"
            ]
        }
  ]
}
EOF
}

data "aws_iam_policy" "sagemaker_full_access_policy" {
  arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

data "aws_iam_policy" "Imagebuilder_policy" {
  arn = "arn:aws:iam::aws:policy/EC2InstanceProfileForImageBuilderECRContainerBuilds"
}


resource "aws_iam_role_policy_attachment" "s3policy-attach-to-role" {
  role       = aws_iam_role.sagemaker_role_name.name
  policy_arn = aws_iam_policy.policy.arn
}

resource "aws_iam_role_policy_attachment" "SagemakerPolicy-attach-to-role" {
  role       = aws_iam_role.sagemaker_role_name.name
  policy_arn = data.aws_iam_policy.sagemaker_full_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "ImagebuilderPolicy-attach-to-role" {
  role       = aws_iam_role.sagemaker_role_name.name
  policy_arn = data.aws_iam_policy.Imagebuilder_policy.arn
}

# S3 Bucket Initialization
resource "aws_s3_bucket" "s3" {
  bucket = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_acl" "s3" {
  bucket = aws_s3_bucket.s3.id
  acl    = "public-read-write"
}

# Mysql Server Initialization
resource "aws_db_instance" "mysql" {
  identifier           = var.identifier
  allocated_storage    = var.allocated_storage
  engine               = var.engine
  engine_version       = var.engine_version
  instance_class       = var.instance_class
  db_name              = var.mysql_db_name
  username             = var.mysql_username
  password             = var.mysql_password
  parameter_group_name = var.parameter_group_name
  skip_final_snapshot  = var.skip_final_snapshot
  vpc_security_group_ids = [aws_security_group.security_group.id]
  publicly_accessible = var.publicly_accessible
}

# Ec2 Server Configuration
resource "aws_security_group" "ec2-server-security-group" {
  name        = "ec2-server-security-group"
  description = "Allow All Traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    from_port        = 8080
    to_port          = 8080
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "mlops-mysql-security-group"
  }
}

# Role Attachment with ec2 instance
resource "aws_iam_instance_profile" "ec2-instance-role-attach" {
  name = "ec2-instance-role-server"
  role = aws_iam_role.sagemaker_role_name.name
}

resource "aws_instance" "ec2-instance-server" {
  ami = var.ami
  instance_type = var.instance_type
  #availability_zone = [var.availability_zone]
  key_name = var.key_name
  security_groups = ["ec2-server-security-group"]
  iam_instance_profile = aws_iam_instance_profile.ec2-instance-role-attach.name
}


