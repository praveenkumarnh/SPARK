#!/bin/bash

export BUILD_TYPE="debug"
export BUILD_ROOT=$PWD/builds
export DEPLOY_ROOT=$PWD/deploy
export BUILD_NAME="linux_coverage"
export BUILD_VARIANT="variant_linux_coverage"
export BUILD_COMPONENTS="linux_coverage_components"
export SOURCE_DIR="$PWD/src"
export BUILD_DIR="$PWD/builds/$BUILD_NAME"
export DEPLOY_DIR="$PWD/deploy/$BUILD_NAME"
export CFG_DIR="$PWD/config"

python buildtools/build.py $BUILD_COMPONENTS $BUILD_VARIANT clean-all all
rm -r $BUILD_DIR/report
mkdir $BUILD_DIR/report
python buildtools/CoverageReport.py $BUILD_COMPONENTS
