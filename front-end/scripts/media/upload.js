import { getToken } from '../auth/index.js';

export async function uploadFile(file) {
    const formData = new FormData();

    formData.append('file', file);

    const headers = {};

    const token = getToken();

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const res = await fetch('/media/upload', {
        method: 'POST',
        headers,
        body: formData
    });

    if (!res.ok) {
        throw new Error(
            `Upload failed: ${res.statusText}`
        );
    }

    return res.json();
}

export async function getFileMetadata(id) {
    const res = await fetch(`/media/files/${id}`);

    return res.json();
}
