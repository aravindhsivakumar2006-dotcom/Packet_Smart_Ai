async function api(
    url,
    options = {}
) {

    const opts = {
        ...options,

        headers: {
            ...(options.headers || {})
        }
    };


    if (
        options.body &&
        typeof options.body === "string"
    ) {

        opts.headers[
            "Content-Type"
        ] = "application/json";

    }


    return fetch(
        url,
        opts
    );
}


function escapeHtml(
    value
) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        function (match) {

            return {

                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#039;"

            }[match];

        }
    );
}


function money(
    value
) {

    return "₹" +
        Number(
            value || 0
        ).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 0
            }
        );
}


function renderResults(
    data
) {

    const allocations =
        (data.allocations || [])
            .map(
                allocation => `

                    <div>

                        <b>
                            ${escapeHtml(
                                allocation.category
                            )}
                        </b>

                        <br>

                        ${money(
                            allocation.amount
                        )}

                        <br>

                        <small>
                            ${
                                allocation.percentage
                                || 0
                            }%
                        </small>

                    </div>

                `
            )
            .join("");


    const recommendations =
        (data.recommendations || [])
            .map(
                item => `

                    <article class="rec">

                        <h4>
                            ${escapeHtml(
                                item.name
                            )}
                        </h4>

                        <small>

                            ${escapeHtml(
                                item.category
                                || ""
                            )}

                            ·

                            ${escapeHtml(
                                item.platform
                                || ""
                            )}

                        </small>


                        <p class="price">

                            ${money(
                                item.estimated_price
                            )}

                        </p>


                        <a
                            target="_blank"
                            rel="noopener"
                            href="${item.link}"
                        >

                            Search on
                            ${escapeHtml(
                                item.platform
                                || "platform"
                            )}

                            →

                        </a>

                    </article>

                `
            )
            .join("");


    const tips =
        (data.tips || [])
            .map(
                tip => `

                    <li>
                        ${escapeHtml(tip)}
                    </li>

                `
            )
            .join("");


    document
        .querySelector("#results")
        .innerHTML = `

            <section class="card">

                <div class="result-head">

                    <div>

                        <span class="pill">

                            ${escapeHtml(
                                data.source
                                || "AI"
                            )}

                        </span>


                        <h2>
                            Recommendation plan
                        </h2>


                        <p>

                            ${escapeHtml(
                                data.summary
                                || ""
                            )}

                        </p>

                    </div>


                    <b>

                        ${money(
                            data.budget
                        )}

                    </b>

                </div>


                <h3>
                    Budget allocation
                </h3>


                <div class="alloc">

                    ${allocations}

                </div>


                <h3>
                    Suggestions
                </h3>


                <div class="rec-grid">

                    ${
                        recommendations
                        ||
                        "<p>No suggestions returned.</p>"
                    }

                </div>


                <h3>
                    Tips
                </h3>


                <ul>

                    ${tips}

                </ul>

            </section>

        `;
}


(async function () {

    try {

        const response =
            await api(
                "/api/auth/me"
            );


        const link =
            document.querySelector(
                "#authLink"
            );


        if (
            response.ok &&
            link
        ) {

            link.textContent =
                "Logout";


            link.href =
                "#";


            link.onclick =
                async function (event) {

                    event.preventDefault();


                    await api(
                        "/api/auth/logout",
                        {
                            method: "POST"
                        }
                    );


                    location.href =
                        "/";

                };

        }

    } catch (error) {

        console.error(error);

    }

})();