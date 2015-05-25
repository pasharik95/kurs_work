function basic_pie(container, x1, x2) {
  var
    d1 = [[0, x2]],
    d2 = [[0, x1]],
    graph;

  graph = Flotr.draw(container, [
    { data : d1, label : 'Прийнято участь в аукціонах' },
    { data : d2, label : 'Виграно аукціонів' },
  ], {
    HtmlText : false,
    grid : {
      verticalLines : false,
      horizontalLines : false
    },
    xaxis : { showLabels : false },
    yaxis : { showLabels : false },
    pie : {
      show : true,
      explode : 6
    },
    mouse : { track : true },
    legend : {
      position : 'se',
      backgroundColor : '#D2E8FF'
    }
  });
  };