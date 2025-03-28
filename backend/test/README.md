# libs
pip install pytest pytest-asyncio pytest-cov

# run test
python -m pytest

To see test coverage (what percentage of your code is tested):
python -m pytest --cov=app tests/

For a detailed report on coverage:

python -m pytest --cov=app --cov-report=html tests/