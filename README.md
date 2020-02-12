# GIB experiment

## Build Setup

``` bash
# install dependencies
npm install
pip install -r requirement.txt

# setup the server
python init_dev.py

# run server
python server.py

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build
```

## Generate TRGIB layouts

``` bash
# change directory
cd data_generation/py

# run program
python run.py
```

### data generation
./data_generation

### experiment
./src

### server
./server.py and ./flaski