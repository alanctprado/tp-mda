#!/usr/bin/sh

# INITIAL SETUP ----------------------------------------------------------------
PROJECT_ROOT=$(realpath $(dirname $0))
DATA_DIR="$PROJECT_ROOT/data"
VENV_DIR="$PROJECT_ROOT/venv"
SCRIPT_DIR="$PROJECT_ROOT/scripts"

echo $DATA_DIR

if [ ! -d $DATA_DIR ]
then
    mkdir $DATA_DIR
    echo "Created data directory at $DATA_DIR"
else
    echo "Found data directory at $DATA_DIR"
fi

if [ ! -d $VENV_DIR ]
then
    echo "Creating Python virtual environment..."
    python3 -m venv $VENV_DIR
    echo "Created Python virtual environment at $VENV_DIR"
else
    echo "Found Python virtual environment at $VENV_DIR"
fi
source $VENV_DIR/bin/activate

echo "Checking and installing Python dependencies..."
pip freeze > req.txt
echo "Done!"

export MDABASEDIR=$PROJECT_ROOT
export MDADATADIR=$DATA_DIR
export MDASCRIPTDIR=$SCRIPT_DIR

# GET CONTEST DATA -------------------------------------------------------------
echo "Getting contest data..."
python $SCRIPT_DIR/get_contests.py
echo "Done!"

# GET ALL USERS ----------------------------------------------------------------
echo "Getting user data..."
sh $SCRIPT_DIR/get_users.sh
echo "Done!"

# GET ACTIVE USERS -------------------------------------------------------------
echo "Getting active users data..."
python $SCRIPT_DIR/get_active_users.py
echo "Done!"

# GET ACTIVE USERS' SUBMISSIONS ------------------------------------------------
echo "Getting submissions for active users..."
sh $SCRIPT_DIR/get_submissions.sh
echo "Done!"

echo "All data was downloaded successfully! :)"
