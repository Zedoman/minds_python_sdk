name: Build and publish to PyPi

on:
  release:
    types: [published]

jobs:
 #  Push a new release to PyPI
  deploy_to_pypi:
    name: Publish to PyPI
    runs-on: ubuntu-latest
    if: github.actor != 'mindsdbadmin'
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5.1.0
        with:
          python-version: ${{ vars.CI_PYTHON_VERSION }}
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install setuptools wheel twine
      - name: Clean previous builds
        run: rm -rf dist/
      - name: Build and publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
        run: |
          # This uses the version string from __about__.py, which we checked matches the git tag above
          python setup.py sdist
          twine upload dist/*