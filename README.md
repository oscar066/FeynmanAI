# FeynmanAi

FeynmanAi is a command-line tool for using the Retrieval Augmented Generation (RAG) model on local documents. It allows you to query your documents and get answers, as well as quiz yourself on the document contents.

## Installation

You can install FeynmanAi using pip:

```bash
pip install FeynmanAI
```

## Usage

The `FeynmanAi` package provides a command-line interface (CLI) that you can use to interact with the RAG model and your local documents.

### Interactive Query Loop

To start the interactive query loop, run the following command:

```bash
FeynmanAi -d /path/to/your/document.pdf 
```

This will add the specified document to the model's knowledge base and enter the interactive query loop.

In the interactive query loop, you can enter questions, and the tool will provide answers based on the documents you've added. Here are the available commands:

- `Enter your question (or 'quit' to exit, 'clear' to clear screen):`: Type your question, and the tool will retrieve an answer from the RAG model.
- `'quit'`: Exit the interactive query loop.
- `'clear'`: Clear the screen and continue the interactive session.

### Quiz Mode

You can also enter quiz mode by using the `-qz` or `--quiz` flag:

In quiz mode, the tool will randomly select a topic from your documents and ask you a question related to that topic. You can type your answer, and the tool will provide feedback.

To exit quiz mode, type `'quit'`.

### Other Options

The `FeynmanAi` package also provides the following additional options:

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