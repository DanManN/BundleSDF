source source_me
DIR=DATA1
# 1) Run joint tracking and reconstruction
# python run_custom.py --mode run_video --video_dir $DIR --out_folder outputs/$DIR --use_segmenter 1 --use_gui 0 --debug_level 2

# 2) (Optinal) Run global refinement post-processing to refine the mesh
python run_custom.py --mode global_refine --video_dir $DIR --out_folder outputs/$DIR

# 3) Get the auto-cleaned mesh
python run_custom.py --mode get_mesh --video_dir $DIR --out_folder outputs/$DIR
