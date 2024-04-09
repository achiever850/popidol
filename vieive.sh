#!/bin/bash

# Default configuration file

ROOT_PATH=""
SCRIPT_PATH=""
LOG_PATH=""
CONFIG_FILE="$SCRIPT_PATH/config_functions.sh"

# Function to display usage instructions
usage() {
    echo "Usage:"
    echo "$0 -config <key>            # to use configurations from the config file"
    echo "$0 -source <path> -target <path> -pattern <pattern> # to specify arguments directly"
    echo "$0 <source> <target> <pattern>   # to use positional arguments"
    exit 1
}

# Function to read configurations from the config file
use_config() {
    local key=$1
    if source "$CONFIG_FILE" && declare -f "$key" > /dev/null; then
        $key
    else
        echo "Error: Configuration for '$key' not found in $CONFIG_FILE."
        exit 1
    fi
}

# Function to parse named arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -source)
                SOURCE_PATH="$2"
                shift # past argument
                shift # past value
                ;;
            -target)
                TARGET_PATH="$2"
                shift # past argument
                shift # past value
                ;;
            -pattern)
                FILE_PATTERN="$2"
                shift # past argument
                shift # past value
                ;;
            -config)
                use_config "$2"
                shift # past argument
                shift # past value
                return 0
                ;;
            *) # unknown option
                usage
                ;;
        esac
    done
}

# Main program

# Check if no arguments were provided
if [ $# -eq 0 ]; then
    usage
fi

# Parse named arguments or use the configuration key
if [[ "$1" =~ ^- ]]; then
    parse_args "$@"
else
    # Check if the right number of positional arguments are provided
    if [ $# -ne 3 ]; then
        usage
    fi
    SOURCE_PATH="$1"
    TARGET_PATH="$2"
    FILE_PATTERN="$3"
fi

# Validate that the required arguments are set
if [ -z "$SOURCE_PATH" ] || [ -z "$TARGET_PATH" ] || [ -z "$FILE_PATTERN" ]; then
    usage
fi


# Function to initialize logging
initialize_logging() {
    timestamp=$(date +"%Y%m%d-%H%M%S")
    # Clean FILE_PATTERN for use in filename: remove wildcard characters like '*'
    clean_file_pattern=$(echo "$FILE_PATTERN" | tr -d '*')
    # Use a generic name if FILE_PATTERN is empty
    log_file_base_name=${clean_file_pattern:-"Archive"}
    # Create the log file name with the cleaned-up pattern and timestamp
    log_file="$log_dir/archive_${log_file_base_name}_$timestamp.log"
    touch "$log_file"
    echo "$(date) - Script started" | tee -a "$log_file"
}

# Function to check for files and move them
move_files() {
    local subdirectory=$1
    local pattern=$2
    local exists=false
    local count=0

    echo "$(date) - Checking for files in $subdirectory with pattern $pattern." | tee -a "$log_file"

    # Check if files exist in the subdirectory
    for file in "$SOURCE_PATH/$subdirectory/$pattern"; do
        if [ -f "$file" ]; then
            exists=true
            ((count++))
        fi
    done

    # Move files if they exist
    if $exists; then
        echo "$(date) - Moving $count file(s) from $subdirectory to archival/$subdirectory." | tee -a "$log_file"
        mv "$SOURCE_PATH/$subdirectory/$pattern" "$TARGET_PATH/$subdirectory" && \
        echo "$(date) - Move successful." | tee -a "$log_file" || \
        echo "$(date) - ERROR: Move failed." | tee -a "$log_file"
    else
        echo "$(date) - No $pattern files found in $subdirectory." | tee -a "$log_file"
    fi
}

# Main script starts here

# Initialize logging
initialize_logging

echo "$(date) - Starting file operations with SOURCE_PATH: $SOURCE_PATH, TARGET_PATH: $TARGET_PATH, FILE_PATTERN: $FILE_PATTERN" | tee -a "$log_file"

# Check for empty parameters
if [ -z "$SOURCE_PATH" ] || [ -z "$TARGET_PATH" ] || [ -z "$FILE_PATTERN" ]; then
    echo "$(date) - ERROR: Parameters cannot be empty" | tee -a "$log_file"
    exit 1
fi

# Move files for different subdirectories
move_files "blackrock" "$FILE_PATTERN"
move_files "encryption" "$FILE_PATTERN"


echo "$(date) - Script Completed" | tee -a "$log_file"
