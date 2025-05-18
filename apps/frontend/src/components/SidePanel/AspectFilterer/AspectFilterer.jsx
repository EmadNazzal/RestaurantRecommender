import React from 'react';
import { Autocomplete, TextField } from '@mui/material';
import styles from '../SidePanel.module.css'; // Import the CSS module

function AspectFilterer({ aspects, onAspectSelection }) {
  const options = aspects.map(aspect => ({ value: aspect, label: aspect }));

  const handleChange = (event, selectedOptions) => {
    const values = selectedOptions.map(option => option.value);
    onAspectSelection(values);
  };

  return (
    <div className={styles.selectBase}>
      <Autocomplete
        multiple
        options={options}
        getOptionLabel={(option) => option.label}
        onChange={handleChange}
        renderInput={(params) => (
          <TextField
            {...params}
            variant="outlined"
            placeholder="Select Aspects"
            fullWidth
          />
        )}
      />
    </div>
  );
}

export default AspectFilterer;
