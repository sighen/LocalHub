export function resolvePlaceImageCandidates(place) {
  if (!place || typeof place !== 'object') return []
  // Common names used across seed data / APIs.
  // image_url (TourAPI firstimage) is prioritized over thumbnail_url
  // (firstimage2) because the upstream thumbnail file is frequently
  // missing from the CDN even when the full-size image exists.
  const candidates = [
    place.image_url,
    place.thumbnail_url,
    place.image,
    place.thumbnail,
    place.firstimage,
    place.firstimage2,
    Array.isArray(place.images) && place.images[0],
    Array.isArray(place.imageList) && place.imageList[0],
  ]

  return [...new Set(candidates.filter(Boolean))]
}

export function resolvePlaceImage(place) {
  const [first] = resolvePlaceImageCandidates(place)
  return first || null
}
