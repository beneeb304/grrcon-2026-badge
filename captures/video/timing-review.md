# LED recording timing review

The reattached files are the original IMG_5316.mov and IMG_5318.mov, not new controlled restart recordings. Both are approximately 29.98 fps. Resampled at 30 samples per second from 12 seconds onward, using aggregate bright green pixels in the badge region. This measures aggregate flashes, not a complete per-LED decode. Static indicator light and movement affect thresholds.

- 5316: 1029 samples; median aggregate lit interval 0.30s, median dim interval 0.10s. Across thresholds 160–300, the main lit intervals cluster around 0.2–0.4s and dim intervals around 0.07–0.17s.
- 5318: 1230 samples; median aggregate lit interval 0.30s, median dim interval 0.10s. Across thresholds 160–300, the main lit intervals cluster around 0.2–0.4s and dim intervals around 0.07–0.17s.

No clear short/long Morse split or long letter/word pauses was established from aggregate brightness. This does not rule out an individual LED or simultaneous LED group encoding. Earlier per-group extraction was sampled only every quarter second and is inadequate to establish that. A fixed-camera capture of repeatable startup sequences remains preferable to guessing a text decode.
