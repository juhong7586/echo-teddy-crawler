# Echo Teddy Crawler

This project is a web crawler designed to scrape exam questions and answers from the ITExams website for the BCBA exam. The crawler uses Selenium and BeautifulSoup to navigate through the pages and extract the necessary data.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.6 or later.
- You have installed the required Python packages:
  - `pandas`
  - `beautifulsoup4`
  - `selenium`
- You have Google Chrome installed.
- You have the ChromeDriver installed and added to your system PATH.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your-username/echo-teddy-crawler.git
    cd echo-teddy-crawler
    ```

2. Install the required Python packages:

    ```bash
    pip install pandas beautifulsoup4 selenium
    ```

3. Download the Chrome extension and place it in the specified folder:

    ```plaintext
    /Users/juhong/Library/Application Support/Google/Chrome/Default/Extensions/mpbjkejclgfgadiemmefgebjfooflfhl/3.1.0_0.crx
    ```

## Usage

1. Open the `crawler_echo.py` file and update the `url` variable if necessary:

    ```python
    url = "https://www.itexams.com/exam/BCBA"
    ```

2. Run the script:

    ```bash
    python crawler_echo.py
    ```

3. Enter the number of pages you want to crawl when prompted.

4. The script will navigate through the pages, solve reCAPTCHA challenges, and extract the questions and answers. The data will be saved to a CSV file named `bcba_exam_questions.csv`.

## Project Structure

- `crawler_echo.py`: The main script that contains the web crawler logic.
- `README.md`: This file.

## Functions

### `is_valid_num_pages(num_pages)`

Validates the user input for the number of pages to crawl.

### `get_user_input()`

Prompts the user to enter the number of pages to crawl and validates the input.

### `page_crawler(html, QA_data)`

Parses the HTML content of a page and extracts the questions and answers.

### `move_around(button_xpath)`

Navigates to the next page by clicking the "Next Page" button and solving reCAPTCHA challenges if necessary.

## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Acknowledgements

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Selenium](https://www.selenium.dev/)
- [ITExams](https://www.itexams.com/)
