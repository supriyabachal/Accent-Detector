.PHONY : train

train :
	python train.py \
		--data_url= \
		--how_many_training_steps='5,5' \
		--learning_rate='0.01,0.01' \
		--batch_size=50 \
		--eval_step_interval=5 \
		--wanted_words=hindi,english \
		--save_step_interval=5 \
		--data_dir=/Users/raimibinkarim/Desktop/audioproc/data/3-processed-wav \
		--clip_duration_ms=30000 

tensorboard :
	tensorboard --logdir=tmp/retrain_logs &  

clean : 
	rm -r tmp
	pkill -f "tensorboard"

freeze :
	python freeze.py \
		--start_checkpoint=tmp/speech_commands_train/conv.ckpt-5 \
		--output_file=tmp/my_frozen_graph.pb \
		--wanted_words=hindi,english \
		--clip_duration_ms=30000
	
evaluate :
	python label_wav.py \
		--graph=tmp/my_frozen_graph.pb \
		--labels=tmp/speech_commands_train/conv_labels.txt \
		--wav=/Users/raimibinkarim/Desktop/audioproc/data/3-processed-wav/hindi/10.wav \
		--how_many_labels=2


