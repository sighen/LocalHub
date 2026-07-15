// Normalize image URLs so HTTPS pages don't block http:// resources.
export const secureImageUrl = (url) => {
	if (!url) return null
	const s = String(url).trim()
	if (s.startsWith('//')) return `https:${s}`
	if (s.startsWith('http://')) return s.replace(/^http:\/\//, 'https://')
	return s
}
