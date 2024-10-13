# Convert `webm` to `mp4`

This worked really well for me: `ffmpeg -i screen-capture.webm -c:v copy -c:a aac -b:a 128k output.mp4`.

# Merge 2+ mp4 files together with `ffmpeg`

BTW if you also wanted to concat two or more mp4 files you can do the following:

1. Create a text file called `inputs.txt`.
2. Use file command + each mp4 file path. E.g.

   ```
   file '/home/userName/first.mp4'
   file '/home/userName/second.mp4'
   ```

   Remember that the order here matters. In this example it will append the `second.mp4` to `first.mp4`.

3. `cd` to where this `inputs.txt` is located and execute this command:

   ```
   ffmpeg -f concat -safe 0 -i inputs.txt -c copy output.mp4
   ```
