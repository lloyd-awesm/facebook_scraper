name: Facebook Scraper

on:
  schedule:
    - cron: '0 * * * *'  # Runs every hour
  workflow_dispatch:  # Allows manual triggering

jobs:
  scrape:
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout repository
        uses: actions/checkout@v3

      - name: 🛠 Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: 🏗 Install Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y wget unzip curl
          sudo apt-get install -y chromium-browser chromium-chromedriver
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: 🏃 Run scraper
        env:
          REPORT_URL: ${{ secrets.REPORT_URL }}
        run: python main.py || exit 1

      - name: 📤 Upload Debug Files
        uses: actions/upload-artifact@v4
        with:
          name: debug-files
          path: |
            page_source.html
            table_loaded.png
        if: always()

      - name: 🔄 Commit Changes (if applicable)
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -f facebook_report.csv table_loaded.png page_source.html || echo "No files to add"
          git commit -m "Update Facebook report data" || echo "No changes to commit"
          git push origin main || echo "Nothing to push"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
