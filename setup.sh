set +x
DAY=$1
SOLUTION_DIR=./solutions/$DAY

python ./solutions/get_inputs.py $1
mkdir -p $SOLUTION_DIR
cp ./solutions/template.py $SOLUTION_DIR/run.py
