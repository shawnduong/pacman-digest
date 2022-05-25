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
