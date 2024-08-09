# FeynmanAI

FeynmanAI is a powerful command-line tool that leverages the Retrieval-Augmented Generation (RAG) model to interact with local documents. Whether you want to query your documents for specific information or quiz yourself on the contents, FeynmanAi offers an intuitive interface to get answers and enhance your understanding.

## Features

- **Interactive Query Loop**: Ask questions and get answers based on your documents.
- **Quiz Mode**: Test your knowledge with random questions from your documents.
- **Multi-format Support**: Works with PDF, TXT, PPT, and DOCX files.
- **Additional Options**: Clear the screen after each query or enable text-to-speech for answers.

## Installation

You can install FeynmanAi using pip:

```bash
pip install FeynmanAI
```

## Usage

The `FeynmanAI` package provides a command-line interface (CLI) that you can use to interact with the RAG model and your Local documents.

### Interactive Query Loop

To start the interactive query loop, run the following command:

You can use either `-d` or `--document` flag:

```bash
FeynmanAI -d /path/to/your/document.pdf 
```

#### Example :

The package includes sample documents to get you started :

```bash
FeynmanAI -d Sample_documents/Distributed.pdf
```
This command will load the specified document into the model's knowledge base and initiate the interactive query loop. In this mode, you can ask questions and receive answers derived from the loaded documents. Available commands include:

- `Enter your question (or 'quit' to exit, 'clear' to clear screen):`: Type your question, and the tool will retrieve an answer from the RAG model.
- `'quit'`: Exit the interactive query loop.
- `'clear'`: Clear the screen and continue the interactive session.

### Quiz Mode

You can also enter quiz mode by using the `-qz` or `--quiz` flag:

In quiz mode, the tool will randomly select a topic from your documents and ask you a question related to that topic. You can type your answer, and the tool will provide feedback.

To exit quiz mode, type `'quit'`.

#### Example 

```bash 
FeynmanAI -d Sample_documents/Distributed.pdf -qz
```

### Other Options

The `FeynmanAI` package also provides the following additional options:

- `-cls` or `--clear`: Clear the screen after each query in the interactive mode.
- `-rd` or `--read`: Read the answer out loud (requires text-to-speech capabilities on your system).

## Troubleshooting

If you encounter any issues, please check the error messages and make sure you have the required dependencies installed. If the problem persists, feel free to open an issue on the project's GitHub repository.

## Contributing

If you would like to contribute to the FeynmanAi project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

Please make sure to write tests for any new functionality you add, and ensure that all existing tests pass before submitting your pull request.

## License

FeynmanAi is released under the [MIT License](LICENSE).