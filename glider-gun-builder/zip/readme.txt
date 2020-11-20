Instructions for use of this archive, as of 30 August 2019:

1) Download latest glider guns from https://github.com/ceebo/glider_guns/archive/master.zip

2) Decompress that ZIP archive to a folder, and open that folder.

3) Inside the newly created folder, everything will be inside a subfolder called glider_guns-master.

4) Copy and paste the entire contents of _this_ folder (containing this readme file) --

    glider-gun-builderv2.9.py,
    'template' folder,
    'glider_guns-master' folder (containing just one test file at the moment)
    readme.txt (this file)
    
-- into your newly created folder.  If you've done it right, there should currently be no confirmation
needed for replacing any files.

In your folder you should now have

  glider_guns-master (subfolder)
  template (folder)
  glider-gun-builderv2.9.py
  readme.txt (optional)

5) In Golly, run glider-gun-builderv2.9.py.  New folders 'guns' and 'LHguns' will be created in the
same folder as the script.

----------------------------------

The script works according to the current README, so if the ceebo/glider_guns repository has been
updated since 30 August 2019, the script may report (as "missing") some revised guns that it is
unable to build.  Otherwise you should eventually see a summary saying that 1011 gun patterns
have been created successfully.

TODO:  figure out whether /specialcases/p00550osc5_15_p00335,0,0,0.rle is used for anything...
       ... given that it doesn't contain the key infix _special_.  Probably the problem that
       it represents has gotten solved by template/p00550osc5alt15,0,0,0.rle?