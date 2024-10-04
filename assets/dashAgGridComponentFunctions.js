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