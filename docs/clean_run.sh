rm -rf ./source
make clean

python generate_docs.py ../src/animation/manim_env ../src/animation/media/ ../src/animation/datas ../src/forces/datas/ ../src/forces/experiments ../src/Neuroscience/tests ../src/unitree_legged_sdk/build/ ../src/unitree_legged_sdk/example/ ../src/unitree_legged_sdk/include/ ../src/unitree_legged_sdk/lib/ ../src/unitree_legged_sdk/example_py/Bezier/deprecated/ ../src/unitree_legged_sdk/example_py/old_examples #../src/animation/ #à remettre à la fin, à faire en dernier car prend beaucoup de temps.
python index_append.py
# then you got to remove the line "source/index" in the index.rst file, and the source/index.rst file.