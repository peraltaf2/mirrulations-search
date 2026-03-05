export async function searchDockets(query, docket_type = '', agency = '', cfr_part = '', page = 1) {
    // EncodeURIComponent allows for spaces, special chars, etc
	const response = await fetch(
        `/search/?str=${encodeURIComponent(query)}&docket_type=${encodeURIComponent(docket_type)}&agency=${encodeURIComponent(agency)}&cfr_part=${encodeURIComponent(cfr_part)}&page=${page}`
    )

	if (!response.ok) {
		throw new Error(`Search request failed: ${response.status}`)
	}

	const results = await response.json()

	const pagination = {
		page: Number(response.headers.get("X-Page")),
		pageSize: Number(response.headers.get("X-Page-Size")),
		totalResults: Number(response.headers.get("X-Total-Results")),
		totalPages: Number(response.headers.get("X-Total-Pages")),
		hasNext: response.headers.get("X-Has-Next") === "true",
		hasPrev: response.headers.get("X-Has-Prev") === "true",
	  }
	  console.log("results", results)
	  console.log("pagination", pagination)
	return { results, pagination }
}

