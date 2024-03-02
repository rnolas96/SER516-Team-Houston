import React from 'react';
import { ReactComponent as BoxPlotSvg } from '../svg/box-plot.svg';

const iconsMap = {
    boxplot: BoxPlotSvg
};

const SvgIcon = ({ className, name, ...others }) => {
  const Component = iconsMap[name];

  if (!Component) {
    return <div />;
  }

  return React.cloneElement(<Component data-testid="svg-icon" />, {
    className,
    ...others
  });
};

export default SvgIcon;