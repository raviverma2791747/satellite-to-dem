var s2SrMain = ee.ImageCollection("COPERNICUS/S2_SR");
var s2CloudsMain = ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY");

var START_DATE = ee.Date("2019-01-01");
var END_DATE = ee.Date("2019-03-01");
var MAX_CLOUD_PROBABILITY = 65;

var regions = [
  [92.095972222, 25.254027778, 92.595972222, 25.754027778],
  [92.095972222, 24.754027778, 92.595972222, 25.254027778],
  [92.095972222, 24.254027778, 92.595972222, 24.754027778],
  [92.095972222, 23.754027778, 92.595972222, 24.254027778],
  [92.095972222, 23.254027778, 92.595972222, 23.754027778],
  [92.095972222, 22.754027778, 92.595972222, 23.254027778],
  [92.595972222, 25.254027778, 93.095972222, 25.754027778],
  [92.595972222, 24.754027778, 93.095972222, 25.254027778],
  [92.595972222, 24.254027778, 93.095972222, 24.754027778],
  [92.595972222, 23.754027778, 93.095972222, 24.254027778],
  [92.595972222, 23.254027778, 93.095972222, 23.754027778],
  [92.595972222, 22.754027778, 93.095972222, 23.254027778],
  [93.095972222, 25.254027778, 93.595972222, 25.754027778],
  [93.095972222, 24.754027778, 93.595972222, 25.254027778],
  [93.095972222, 24.254027778, 93.595972222, 24.754027778],
  [93.095972222, 23.754027778, 93.595972222, 24.254027778],
  [93.095972222, 23.254027778, 93.595972222, 23.754027778],
  [93.095972222, 22.754027778, 93.595972222, 23.254027778],
  [93.595972222, 25.254027778, 94.095972222, 25.754027778],
  [93.595972222, 24.754027778, 94.095972222, 25.254027778],
  [93.595972222, 24.254027778, 94.095972222, 24.754027778],
  [93.595972222, 23.754027778, 94.095972222, 24.254027778],
  [93.595972222, 23.254027778, 94.095972222, 23.754027778],
  [93.595972222, 22.754027778, 94.095972222, 23.254027778],
  [94.095972222, 25.254027778, 94.595972222, 25.754027778],
  [94.095972222, 24.754027778, 94.595972222, 25.254027778],
  [94.095972222, 24.254027778, 94.595972222, 24.754027778],
  [94.095972222, 23.754027778, 94.595972222, 24.254027778],
  [94.095972222, 23.254027778, 94.595972222, 23.754027778],
  [94.095972222, 22.754027778, 94.595972222, 23.254027778],
  [94.595972222, 25.254027778, 95.095972222, 25.754027778],
  [94.595972222, 24.754027778, 95.095972222, 25.254027778],
  [94.595972222, 24.254027778, 95.095972222, 24.754027778],
  [94.595972222, 23.754027778, 95.095972222, 24.254027778],
  [94.595972222, 23.254027778, 95.095972222, 23.754027778],
  [94.595972222, 22.754027778, 95.095972222, 23.254027778],
];

function maskClouds(img) {
  var clouds = ee.Image(img.get("cloud_mask")).select("probability");
  var isNotCloud = clouds.lt(MAX_CLOUD_PROBABILITY);
  return img.updateMask(isNotCloud);
}

// The masks for the 10m bands sometimes do not exclude bad data at
// scene edges, so we apply masks from the 20m and 60m bands as well.
// Example asset that needs this operation:
// COPERNICUS/S2_CLOUD_PROBABILITY/20190301T000239_20190301T000238_T55GDP
function maskEdges(s2_img) {
  return s2_img.updateMask(
    s2_img.select("B8A").mask().updateMask(s2_img.select("B9").mask())
  );
}

for (var i = 0; i < regions.length; i++) {
  // Filter input collections by desired data range and region.
  var criteria = ee.Filter.and(
    ee.Filter.bounds(
      ee.Geometry.Rectangle({ coords: regions[i], geodesic: false })
    ),
    ee.Filter.date(START_DATE, END_DATE)
  );
  var s2Sr = s2SrMain.filter(criteria).map(maskEdges);
  var s2Clouds = s2CloudsMain.filter(criteria);

  // Join S2 SR with cloud probability dataset to add cloud mask.
  var s2SrWithCloudMask = ee.Join.saveFirst("cloud_mask").apply({
    primary: s2Sr,
    secondary: s2Clouds,
    condition: ee.Filter.equals({
      leftField: "system:index",
      rightField: "system:index",
    }),
  });

  var s2CloudMasked = ee
    .ImageCollection(s2SrWithCloudMask)
    .map(maskClouds)
    .median();
  //var rgbVis = {min: 0, max: 3000, bands: ['B4', 'B3', 'B2']};

  //Map.addLayer(
  //    s2CloudMasked, rgbVis, 'S2 SR masked at ' + MAX_CLOUD_PROBABILITY + '%',
  //    true);
  //

  Export.image.toDrive({
    image: s2CloudMasked,
    description: "image_tile_"+i.toString(),
    folder: "ee_demos",
    region:  ee.Geometry.Rectangle({ coords: regions[i], geodesic: false }),
    scale: 10,
  });
}
