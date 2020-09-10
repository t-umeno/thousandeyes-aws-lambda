# thousandeyes-aws-lambda
* ThousandEyes API v6を用いてEnterprise Agentの状態を取得します。Enterprise AgentがofflineになったらLINE Notify で通知します。  
* AWS EventBridgeからAWS Lambdaを定期実行し、Enterprise Agentがofflineになったら現在の状態を保存するためにAWS S3にファイルを作成します。  
![diagram](https://github.com/t-umeno/thousandeyes-aws-lambda/blob/master/diagram.png)

## 実行方法
以下、前提条件です。  
* AWS, ThousandEyes, LINEのアカウントは取得済  
* AWS はオレゴン(米国西部) us-west2 リージョンを使用、リージョンを変更する際にはリージョンに関する部分を変更して実行してください。  
* S3 バケット名は thousandeyes-agent とした記載です。バケット名を変更する際はバケット名に関する部分を変更して実行してください。  

1. Ubuntu 18.04 LTS 環境を用意します。  
[Ubuntu 18.04.5 LTS (Bionic Beaver)](https://releases.ubuntu.com/18.04.5/)からISOイメージなどを入手し、パソコンやVirtualBoxなどの環境でUbuntu 18.04 LTSをインストールします。

1. Ubuntu 18.04 LTS 上に AWS CLI バージョン2 をインストールします。  
[Linux での AWS CLI バージョン 2 のインストール](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/install-cliv2-linux.html) の記載に従って AWS CLI バージョン2をインストールします。

1. AWS IAM グループ AdministratorGroup 作成  
[AWS IAM グループ](https://console.aws.amazon.com/iam/home#/groups) で「新しいグループの作成」ボタンを押し、グループ名に「AdministratorGroup」を指定し、「ポリシーのアタッチ」で「AdministratorAccess」を選択したグループを作成します。

1. AWS IAM ユーザー administrator 作成  
[AWS IAM ユーザー](https://console.aws.amazon.com/iam/home#/users) で「ユーザーを追加」ボタンを押し、「ユーザー詳細の設定」の「ユーザー名」に「administrator」を入力、「プログラムによるアクセス」にチェックし、「次のステップ: アクセス権限」
を押し、「ユーザーをグループに追加」で「AdministratorGroup」にチェックを押し、「次のステップ: タグ」を押し、「次のステップ: 確認」を押し、「ユーザーの作成」を押して、ユーザーを作成します。

1. AWS CLI バージョン 2 の設定を行います。  
[設定の基本](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-quickstart.html) に沿ってAWS CLI バージョン 2 の設定を行います。  
[アクセスキー ID とシークレットアクセスキー](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds)に記載された方法で administrator の アクセスキー ID とシークレットアクセスキー を入手します。  
administrator の アクセスキー ID とシークレットアクセスキー を用いて[aws configure を使用したクイック設定](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) に沿って設定を行います。Default region name には us-west-2、 Default output format には json を指定してください。

1. Ubuntu 18.04 LTS に virtualenv, zip をインストール  

1. ThousandEyes の Enterprise Agentを設置  
ThousandEyes にログインし [Get Started with Devices](https://app.thousandeyes.com/settings/devices/) の「Install More Agents」のボタンを押して、 Enterprise Agent の OVA ファイルを入手します。入手した OVA ファイルを VirtualBox などにインストールします。  
ThousandEyes の Enterprise Agent の Enterprise Agent の詳細は [What is an Enterprise Agent?](https://success.thousandeyes.com/PublicArticlePage?articleIdParam=kA0E0000000CmnbKAC_What-is-an-Enterprise-Agent-1472236187506) を参照してください。  
エージェント名を thousandeyes-va から変更する場合、エージェント名を控えておいてください。  

1. ThousandEyes の Token を取得します。  

1. LINE Notify アクセストークンの発行  
[LINE Notify マイページ](https://notify-bot.line.me/ja/)でアクセストークンを発行します。

1. AWS IAM ロール lambda-s3fullaceess-role 作成  
[AWS IAM ロール](https://console.aws.amazon.com/iam/home?#/roles) で
「ロールの作成」ボタンを押し、ポリシーに下記をアタッチした lambda-s3fullaceess-role というロールを作成します。
    * AmazonS3FullAccess  
    * AWSLambdaExecute  

1. AWS S3 バケット thousandeyes-agent 作成  
現在の状態を保存するS3バケットを作成します。  
[AWS S3](https://s3.console.aws.amazon.com/s3/home) で
「＋バケットを作成する」を押し、
バケット名 「thousandeyes-agent」を入力し、
リージョン　「オレゴン(米国西部)」を選択、
「次へ」を3回押して、「バケットを作成」を押します。

1. make_function_zip.sh 実行  
    AWS Lambda で実行するプログラムを function.zip のファイルに集約します。以降、 agents のディレクトリでコマンド実行します。
    ```
    cd agents ; ./make_function_zip.sh

    ```
1. create-function.sh 実行  
    AWS Labmda に実行するプログラムをアップロードします。
    * AWS アカウント ID 123456789012  
    * S3 バケット thousandeyes-agent  
    の場合は下記のコマンドを実行します。
    ```
    ./create-function.sh 123456789012 thousandeyes-agent

    ```

1. env_function.sh 実行  
    AWS Lambda で使用する環境変数を設定します。
    | キー | 値 |
    ----|----
    | THOUSANDEYES_USER | ThousandEyes ユーザ名 |
    | THOUSANDEYES_TOKEN | ThousandEyes Token |
    | LINE_TOKEN | LINE Notify アクセストークン |
    | LINE_OK_MSG | 通信正常になった時に LINE Notify で通知するメッセージ |
    | LINE_NG_MSG | 通信異常になった時に LINE Notify で通知するメッセージ |
    | S3_BUCKET | 現在の状態を保存する S3 バケット |
   
   環境変数が以下の場合、下記のコマンドを実行します。
    | キー | 値 |
    ----|----
    | THOUSANDEYES_USER | taro.yamada@example.com |
    | THOUSANDEYES_TOKEN | 0123456789abcdef0123456789abcdef |
    | LINE_TOKEN | abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG |
    | LINE_OK_MSG | OK |
    | LINE_NG_MSG | NG |
    | S3_BUCKET | thousandeyes-agent |
    ```
    ./env_function.sh \
    THOUSANDEYES_USER=taro.yamada@example.com,\
    THOUSANDEYES_TOKEN=0123456789abcdef0123456789abcdef,\
    LINE_TOKEN=abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG,\
    LINE_OK_MSG=OK,\
    LINE_NG_MSG=NG,\
    S3_BUCKET=thousandeyes-agent
    ```
1. AWS Lambda 設定  
[オレゴンの AWS Lambda > 関数](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions) で 「AgentStatus」をクリックします。デザイナーの「＋トリガーを追加」を押し、「EventBridge (CloudWatch Events)」を選択します。「ルール」で「新規ルールの作成」を選択し、「ルール名」に「agentstatus」を入力し、「ルールタイプ」は「スケジュール式」をチェックし、「スケジュール式」には「cron(0/5 * * * ? *)」を入力し、「トリガーの有効化」のチェックボタンを押して、無効化して「追加」を押します。  
「テスト」を押し、「イベント名」に「test」を入力し、「作成」を押します。再度、「テスト」を押し、「実行結果:成功(ログ)」が表示されることを確認します。
「EventBridge (CloudWatch Events): agentstatus (無効)」のチェックボックスをチェックし、「Enable」ボタンを押し、ダイアログボックスの「Enable」ボタンを押します。ダイアログボックスの「閉じる」を押します。

1. 動作確認  
ThousandEyes の Enterprise Agent とインターネットとの通信を遮断、もしくは Enterprise Agent のVMをシャットダウンして、15分から30分くらいするとLINE NotifyにNGの通知があることを確認します。  
ThousandEyes の Enterprise Agent とインターネットとの通信を回復、もしくは Enterprise Agent のVMを再起動して、数分するとLINE NotifyにOKの通知があることを確認します。  

## 参照
https://developer.thousandeyes.com/v6/  
https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/with-s3-example-deployment-pkg.html#with-s3-example-deployment-pkg-python  
https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-python.html  
https://qiita.com/sunleth/items/bc9fa61866d6f23b3a18  
