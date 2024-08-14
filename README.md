# fridge-scan

## How to run the project

### Setting up Poetry
`pip install poetry`

To enter / create the virtual environment: `poetry shell`

To install the dependencies: `poetry install`

### Setting up environment variables
This project uses an OpenAI API key and a [FreeImage](https://freeimage.host/page/api) API key.

Once you have both, create a `.env` file with these credentials, such as shown in the [.env.example](.env.example)

Then use the command `source .env`

### Using make to run to project
`make run-local`

### Running the project with docker
```
make pull-image
make docker-run-local
```

## Useful links
[Trello of the project](https://trello.com/b/bP43BY6p/gb-final-project)
