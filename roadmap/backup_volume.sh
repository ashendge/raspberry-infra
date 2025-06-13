#!/bin/bash

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_DIR="$HOME/docker-volume-backups"
mkdir -p "$BACKUP_DIR"

docker run --rm \
  -v flask-roadmap-app_db_data:/data \
  -v "$BACKUP_DIR":/backup \
  alpine \
  tar czf /backup/db_backup_$TIMESTAMP.tar.gz -C /data .

echo "Backup saved to $BACKUP_DIR/db_backup_$TIMESTAMP.tar.gz"

# sync to NAS
NAS_BACKUP_DIR="/mnt/nas-backups"
mkdir -p "$NAS_BACKUP_DIR"
rsync -av0 "$BACKUP_DIR/" "$NAS_BACKUP_DIR/" --no-group

# Keep only 7 most recent backups on NAS and local
cd "$NAS_BACKUP_DIR"
ls -tp | grep -v '/$' | tail -n +8 | xargs -r rm --

cd "$BACKUP_DIR"
ls -tp | grep -v '/$' | tail -n +15 | xargs -r rm --