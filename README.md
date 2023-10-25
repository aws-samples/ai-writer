 # AI Writer

This is a Streamlit application that allows users to generate and iteratively revise AI-written articles.

## Functionality

The application has the following functionality:

- Users can provide a prompt to have the AI generate an initial article draft. The generated text is split into paragraphs.

![prompt screenshot](doc/initial_prompt.png)

- The drafted article paragraphs are displayed in a list. Users can click on each paragraph to edit it in a textarea. 

- Below each paragraph textarea is a "Revise" button. Users can provide revise instructions and click this to have the AI revise just that paragraph.
![revise screenshot](doc/revise.png)

- There is an option to provide revise instructions for the entire article, which will invoke the AI to revise all paragraphs.
![whole revise screenshot](doc/whole_revise.png)


- The edited article can be copied out of a final textarea field.


## Setup

Requirements:

- Python 3
- An AWS account with [Amazon Bedrock access](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-console)
	- Make sure you have the required [IAM permission](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-console) and accepted the model [EULAs](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
	- Follow [this guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) to set up the AWS SDK credentails.

```
pip install -r requirements.txt
```

Start the application:

```
streamlit run main.py --server.port 8080
```

Open a browser and navigate to http://localhost:8080 to get started.


## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more infromation

## License

See [LICENSE](LICENSE)
