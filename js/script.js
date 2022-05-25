/* Sort the packages by installed size (largest to smallest). */
data["packages"].sort((a, b) => b[10] - a[10]);

/* Set the packages count. */
$("#pkgs-count").text(data["packages"].length);

/* Calculate the partition usage percentage. */
$("#part-percent").text((100 * data["used"]/data["total"]).toFixed(2) + "%");

/* Generate the partition usage chart. */
const partChart = new Chart(

	document.getElementById("part-chart"),
	{
		type: "pie",
		data:
		{
			labels: ["Used", "Free"],
			datasets:
			[
				{
					label: "Data",
					data:
					[
						(data["used"]/1073741824).toFixed(2),
						((data["total"] - data["used"])/1073741824).toFixed(2),
					],
					backgroundColor: ["#FF0000", "#00FFFF"],
				},
			],
		},
		options:
		{
			plugins:
			{
				legend:
				{
					display: false,
				},
				tooltip:
				{
					callbacks:
					{
						label: (item) => ` ${item.formattedValue} GiB`,
					},
				},
			},
		},
	}
)

/* Create the usage table entries. */
let rows = "";

for (let i = 0; i < (data["packages"].length < 50 ? data["packages"].length : 50); i++)
{
	rows += "<tr><td>" + data["packages"][i][0] + "</td>";
	rows += "<td class='table-data-right'><span class='orange'>" + (data["packages"][i][10]/1048576).toFixed(0) + "</span>";
	rows += " MiB</td></tr>";
}

$("#usage-table tr").first().after(rows)
