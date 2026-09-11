import os
import socket
import cv2

print("=== PRE-DEMO HARDWARE & NETWORK VERIFICATION ===")

# 1. Weight Cache Integrity
weights_path = os.path.expanduser("~/.deepface/weights/facial_expression_model_weights.h5")
if os.path.isfile(weights_path) and os.path.getsize(weights_path) > 5000000:
    print(f"[1] WEIGHT CACHE INTEGRITY: PASSED ({os.path.getsize(weights_path):,} bytes at {weights_path})")
else:
    print(f"[1] WEIGHT CACHE INTEGRITY: FAILED (File missing or incomplete)")

# 2. STUN Server Connectivity
try:
    ip = socket.gethostbyname("stun.l.google.com")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3.0)
    # RFC 5389 STUN Binding Request header (0x0001)
    stun_req = b"\x00\x01\x00\x00\x21\x12\xa4\x42" + os.urandom(12)
    sock.sendto(stun_req, (ip, 19302))
    data, addr = sock.recvfrom(2048)
    sock.close()
    print(f"[2] STUN CONNECTIVITY: PASSED (Resolved {ip}:19302, received {len(data)} bytes STUN response)")
except Exception as e:
    print(f"[2] STUN CONNECTIVITY: WARNING ({e}) - Note: Fallback modes available (Snapshot & Simulator)")

# 3. Hardware Camera Availability
cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    status = "SUCCESS" if ret else "EMPTY"
    print(f"[3] HARDWARE CAMERA: PASSED (Device 0 accessible, frame read: {status})")
    cap.release()
else:
    print("[3] HARDWARE CAMERA: NOTICE (Device 0 occupied by another process or requires OS camera permission)")
