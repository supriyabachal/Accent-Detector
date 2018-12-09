.PHONY: train, noise, clean, remove_ds

resample :
	python resampling.py

noise :
	cp -r data/0-background-noise/_background_noise_ data/2-processed-wav/

remove_ds :
	rm .DS_Store
	rm ./*/.DS_Store
	rm ./*/*/.DS_Store

clean :
	rm -rf data/2-processed-wav

get_top_100 :
	mkdir data/2-processed-wav/american1 data/2-processed-wav/chinese1

