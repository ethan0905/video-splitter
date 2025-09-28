# video-splitter.py
import sys
import os
import subprocess
from pathlib import Path

def split_video(output_folder, video_path, chunk_duration=5):
    out_dir = Path(output_folder)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Sortie : chunk_000.mp4, chunk_001.mp4, ...
    out_pattern = str(out_dir / "chunk_%03d.mp4")

    # Commande ffmpeg robuste pour segments EXACTS de 5s (sauf le dernier)
    cmd = [
        "ffmpeg",
        "-hide_banner", "-loglevel", "error",
        "-i", video_path,

        # ré-encodage vidéo pour forcer des keyframes régulières
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",

        # audio simple et compatible
        "-c:a", "aac",
        "-b:a", "128k",

        # rendre les keyframes déterministes toutes les 5s
        "-force_key_frames", f"expr:gte(t,n_forced*{chunk_duration})",
        "-sc_threshold", "0",

        # découpe en segments
        "-f", "segment",
        "-segment_time", str(chunk_duration),
        "-reset_timestamps", "1",          # évite les écrans noirs / timestamps chelous
        "-map", "0",

        # option utile pour lecture web (pas obligatoire)
        "-movflags", "+faststart",

        out_pattern
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ Découpage terminé dans: {out_dir.resolve()}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 video-splitter.py <output_folder> <path/to/video>")
        sys.exit(1)

    output_folder = sys.argv[1]
    video_path = sys.argv[2]

    if not os.path.isfile(video_path):
        print(f"❌ Fichier introuvable: {video_path}")
        sys.exit(1)

    split_video(output_folder, video_path, chunk_duration=5)

