var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.EditDeleteButton = function (props) {
    const { setData, data } = props;

    function onEditClick() {
        setData({ action: 'edit', rowId: data.Id });
    }

    function onDeleteClick() {
        setData({ action: 'delete', rowId: data.Id });
    }

    function onViewClick() {
        setData({ action: 'view', rowId: data.Id });
    }

    return React.createElement(
        'div',
        // { style: { display: 'flex', justifyContent: 'space-evenly', alignItems: 'center' } },
        {
            style: { 
                display: 'grid',  // Use grid layout
                gridTemplateColumns: 'repeat(2, 1fr)',  // Fixed 2 columns per row
                gap: '10px',  // Space between buttons
                alignItems: 'center',
                justifyContent: 'center',
                width: '100%'  // Allow the grid to take full width
            } ,
        },

        React.createElement(
            'button',
            {
                onClick: onEditClick,
                className: 'edit-btn rounded-full p-[10px] text-md text-white cursor-pointer hover:bg-lightblue-600',
            },
            'Edit'
        ),
        React.createElement(
            'button',
            {
                onClick: onDeleteClick,
                className: 'delete-btn rounded-full p-[10px] text-md text-white cursor-pointer hover:bg-lightred-600',
            },
            'Delete'
        ),
        React.createElement(
            'button',
            {
                onClick: onViewClick,
                className: 'view-btn rounded-full p-[10px] text-md text-white cursor-pointer hover:bg-lightgreen-600',
            },
            'View'
        )
    );
};


dagcomponentfuncs.ImgThumbnail = function (props) {
    const { setData, data } = props;

    function onClick() {
        setData(props.value);
    }

    return React.createElement(
        'div',
        {
            style: {
                width: '100%',
                height: '100%',
                display: 'flex',
                alignItems: 'center',
            },
        },
        React.createElement(
            'img',
            {
                onClick,
                style: { width: '100%', height: 'auto' },
                src: `data:image/jpeg;base64,${props.value}`,
            },
        )
    );
};



// Custom Cell Renderer for displaying color bars based on cell value
dagcomponentfuncs.ColorBarRenderer = function (props) {
    const cellValue = props.value;

    // Define a range for the color bar based on a max and min value
    const colMax = 1;
    const colMin = -1;
    const midpoint = 0;  // Set midpoint to zero to differentiate positive and negative

    // Determine color and percentage based on the cell value
    let color, percentage, leftBarWidth, rightBarWidth;
    
    // Calculate the bar widths based on the value
    if (cellValue >= midpoint) {
        color = '#3D9970'; // Green for values >= 0
        percentage = ((cellValue - midpoint) / (colMax - midpoint)) * 100;
        leftBarWidth = "0%";  // No bar on the left for positive values
        rightBarWidth = `${percentage}%`;  // Right side bar width
    } else {
        color = '#FF4136'; // Red for values < 0
        percentage = ((cellValue - colMin) / (midpoint - colMin)) * 100;
        leftBarWidth = `${percentage}%`;  // Left side bar width
        rightBarWidth = "0%";  // No bar on the right for negative values
    }

    // Create a container with the left and right bars and a text element to show the value
    return React.createElement(
        'div',
        {
            style: {
                width: '100%',
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '2px',
                backgroundColor: '#f4f4f4',  // Light background to highlight the bars
                border: '1px dotted #000'  // Optional: for visual clarity, similar to Excel
            },
        },
        // Left side of the bar (Red for negative values)
        React.createElement(
            'div',
            {
                style: {
                    backgroundColor: cellValue < midpoint ? color : 'transparent',
                    width: leftBarWidth,
                    height: '75%',
                    borderRadius: '2px',
                },
            }
        ),
        // Right side of the bar (Green for positive values)
        React.createElement(
            'div',
            {
                style: {
                    backgroundColor: cellValue >= midpoint ? color : 'transparent',
                    width: rightBarWidth,
                    height: '75%',
                    borderRadius: '2px',
                },
            }
        ),
        // Text element to display the value outside the bar area
        React.createElement(
            'span',
            {
                style: {
                    paddingLeft: '5px',
                    paddingRight: '5px',
                    fontWeight: 'bold',
                    color: '#333',  // Text color
                    minWidth: '35px',  // Fixed width for alignment
                    textAlign: 'right',  // Right align the text
                },
            },
            `${cellValue.toFixed(2)}` // Format the value to 2 decimal places
        )
    );
};

// dagcomponentfuncs.CustomLoadingOverlay = function (props) {
//     return React.createElement(
//         'div',
//         {
//             style: {
//                 border: '1pt solid grey',
//                 color: props.color || 'grey',
//                 padding: 10,
//             },
//         },
//         props.loadingMessage
//     );
// };

// Custom cell renderer for displaying logos with a preview feature
dagcomponentfuncs.LogoRenderer = function (props) {
    // Function to handle the click event for the preview
    function handlePreviewClick(imageUrl) {
        // Create a modal to display the larger image
        const modal = document.createElement('div');
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        modal.style.display = 'flex';
        modal.style.justifyContent = 'center';
        modal.style.alignItems = 'center';
        modal.style.zIndex = '1000';

        // Create the large image element
        const img = document.createElement('img');
        img.src = imageUrl;
        img.style.maxWidth = '90%';
        img.style.maxHeight = '90%';
        img.style.border = '5px solid white';
        img.style.borderRadius = '10px';

        // Append the image to the modal
        modal.appendChild(img);

        // Close the modal when clicked
        modal.addEventListener('click', function() {
            document.body.removeChild(modal);
        });

        // Append the modal to the body
        document.body.appendChild(modal);
    }

    // Create the image element using React.createElement
    const imgElement = React.createElement('img', {
        src: props.value,
        style: { height: '50px', width: 'auto', borderRadius: '5px' }
    });

    // Create the preview icon
    const previewIcon = React.createElement(
        'div',
        {
            style: {
                position: 'absolute',
                top: '5px',
                right: '5px',
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                color: 'white',
                padding: '5px',
                borderRadius: '50%',
                cursor: 'pointer',
                display: 'none'
            },
            onClick: function () {
                handlePreviewClick(props.value);  // Open the larger image in a modal
            }
        },
        '🔍'  // Preview icon (magnifying glass emoji)
    );

    // Container for both the image and the preview icon
    const container = React.createElement(
        'div',
        {
            style: {
                position: 'relative',
                display: 'inline-block'
            },
            onMouseEnter: function () {
                previewIcon.props.style.display = 'block';  // Show preview icon on hover
            },
            onMouseLeave: function () {
                previewIcon.props.style.display = 'none';  // Hide preview icon when mouse leaves
            }
        },
        imgElement, previewIcon  // Append both the image and the preview icon to the container
    );

    return container;
};