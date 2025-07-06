# Jobby

## Overview

Jobby is an automated tool designed to scrape job postings from a job website based on user-defined criteria. It allows users to search for jobs, filter results by location and keywords, export the job offers to a JSON file, and generate personalized PDF presentation cards for each job offer.

## Features

- **Job Search**: Search for jobs on a job website using specific titles and locations.
- **Keyword Filtering**: Detect and extract keywords from job descriptions.
- **Location Filtering**: Filter job offers based on predefined locations.
- **Export Results**: Save job offers to a JSON file for easy access and sharing.
- **PDF Generation**: Create personalized presentation cards for job offers in PDF format.
- **Card Customization**: Use templates with dynamic variables to customize the content of the presentation cards.
- **Debug Mode**: Enable detailed logging for troubleshooting.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/jobby.git
   cd jobby
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and define the following variables:
   ```
   USER_DATA_DIR=path_to_user_data_directory
   DEBUG_MODE=true_or_false
   ```

## Usage

### Launching the Project

You can run the project using one of the following methods:

#### Option 1: Using `PYTHONPATH`
```bash
PYTHONPATH=src python main.py
```

#### Option 2: From the `src` Folder
```bash
cd src
python main.py
```

### Configuration

The project uses a `config.json` file to define search parameters. Place the file in the root directory with the following structure:
```json
{
    "title": "Software Engineer",
    "pages": 2,
    "search_location": "United States",
    "filter_locations": ["California", "New York"],
    "keywords": ["Python", "Django", "Machine Learning"],
    "card_template": "Hello {{name}},\nWe found a job for you at {{company_name}} as a {{job_title}}.\nSkills required: {{skills_list}}.\nPlatform: {{platform}}.",
    "card_language": "en",
    "card_name": "John Doe"
}
```

### Exported Results

The job offers are saved in a JSON file located at:
```
user_data/export.json
```

By default, the `user_data` folder is created inside the project directory. However, you can configure its location by setting the `USER_DATA_DIR` variable in the `.env` file.

### PDF Generation

Presentation cards for job offers are generated in PDF format and saved in:
```
user_data/presentation_cards/
```

The content of the cards is based on the `card_template` defined in the `config.json` file. Dynamic variables such as `{{name}}`, `{{company_name}}`, and `{{skills_list}}` are replaced with actual values.

### Debugging

Enable debug mode by setting `DEBUG_MODE=true` in the `.env` file. This will print detailed logs, including generated URLs and errors.

### Running Tests

To run tests, ensure pytest is installed:
```bash
pip install pytest
```

Run the tests using the following command:
```bash
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Feel free to submit issues or pull requests to improve the project.

## Disclaimer

This tool is intended for educational purposes only. Ensure compliance with the job website's terms of service when using this bot.
