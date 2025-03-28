# Create bucket manual
aws s3api create-bucket --bucket elcliente-deployment-891377403177-us-east-1 --region us-east-1

# other comants deploy

## Delete slak
aws cloudformation delete-stack --stack-name ElCliente-Stack
aws cloudformation wait stack-delete-complete --stack-name ElCliente-Stack

aws cloudformation describe-stack-events --stack-name ElCliente-Stack
aws cloudformation describe-stacks --stack-name ElCliente-Stack --query "Stacks[0].Outputs"
aws iam list-mfa-devices --user-name amaris_deploy --profile amaris_deploy
aws sts get-session-token --serial-number "arn:aws:iam::891377403177:mfa/amaris_deploy" --token-code XXXXXX --profile amaris_deploy


# Asegúrate de estar usando el perfil correcto
$env:AWS_PROFILE = "amaris-deploy"


# Intenta verificar tu identidad
aws sts get-caller-identity

# Verifica que puedes listar stacks de CloudFormation
aws cloudformation list-stacks

# Verifica que puedes listar buckets de S3
aws s3 ls


aws iam list-mfa-devices --user-name amaris_deploy --profile amaris_deploy

# see logs

aws cloudformation describe-stack-events --stack-name ElCliente-Stack
## Especific log
aws cloudformation describe-stack-events --stack-name ElCliente-Stack | findstr CREATE_FAILED


# Eerror

aws cloudformation delete-stack --stack-name ElCliente-Stack
aws cloudformation wait stack-delete-complete --stack-name ElCliente-Stack

# listar politicas y permisos
aws iam get-user
aws iam list-attached-user-policies --user-name TU_NOMBRE_DE_USUARIO

# last recourse
aws iam attach-user-policy --user-name TuUsuario --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# validate template
aws cloudformation validate-template --template-body file://template.yaml

# invalidar cache al ahacer cambios en el labda
aws cloudfront create-invalidation --distribution-id E181VZW9EUQ2JW --paths "/*"

# Verificar logs cloudwatch

aws logs describe-log-streams


aws logs describe-log-streams `
>>   --log-group-name /aws/lambda/ElCliente-Backend-prod `
>>   --order-by LastEventTime `
>>   --descending `
>>   --limit 1 `
>>   --query "logStreams[0].logStreamName"

aws logs describe-log-streams `
  --log-group-name /aws/lambda/ElCliente-Backend-prod `
  --order-by LastEventTime `
  --descending `
  --limit 1 `
  --query "logStreams[0].logStreamName" `
  --output text

"2025/03/27/[$LATEST]f0415dc927644cf6b7cd774d1dace037"

aws logs describe-log-streams --log-group-name /aws/lambda/ElCliente-Backend-prod
aws logs get-log-events --log-group-name /aws/lambda/ElCliente-Backend-prod --log-stream-name '2025/03/27/[$LATEST]f0415dc927644cf6b7cd774d1dace037"'

aws logs get-log-events --log-group-name /aws/lambda/ElCliente-Backend-prod --log-stream-name '2025/03/27/[$LATEST]315ba8aa4e814824a112a0b4416df33a'


aws logs describe-log-groups

#Excanear front
aws s3 ls s3://elcliente-frontend-891377403177-prod/ --recursive

# escanear tablas
aws dynamodb scan --table-name ElCliente-Funds-prod --limit 5
 aws dynamodb scan --table-name ElCliente-Clients-prod --limit 1
aws dynamodb get-item --table-name ElCliente-Clients-prod --key '{"clientId":{"S":"C123456"}}'
    aws dynamodb scan --table-name ElCliente-Funds-prod