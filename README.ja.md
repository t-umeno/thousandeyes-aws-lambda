# thousandeyes-aws-lambda
* ThousandEyes API v6を用いてagentの状態を取得します。agentがofflineになったらLINE Notify で通知します。
* AWS EventBridgeからAWS Lambdaを定期実行し、agentがofflineになったらAWS S3にファイルを作成し、現在の状態を保存します。
